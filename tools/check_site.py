#!/usr/bin/env python3
"""Verifica el sitio público de IRD.

Uso (desde la raíz del proyecto):
    python tools/check_site.py
    python tools/check_site.py --root var/dist
    python tools/check_site.py --allow-missing

Comprueba metadata, hreflang, enlaces internos, imágenes, paridad ES/EN
y cadenas prohibidas. Sale con código 1 si hay errores.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

SITE_HOST = "ird.example"
SKIP_DIRS = {
    ".git", ".superpowers", "_legacy", "admin", "archive", "assets",
    "content", "dist", "docs", "documentos", "herramientas", "Recursos",
    "src", "tools", "var",
}
PAIRS = [
    ("index.html", "en/index.html"),
    ("documento.html", "en/document.html"),
    ("laboratorio.html", "en/lab.html"),
    ("sobre-mi.html", "en/about.html"),
    ("contacto.html", "en/contact.html"),
    ("terminos.html", "en/terms.html"),
]
REQUIRED_HREFLANG = ["es-ar", "en", "x-default"]
BANNED = [
    "ird.com.ar",
    "soluciones.html",
    "producto.html",
    "asistente.html",
    "admin.html",
    "data.js",
    "10 a 15 días",
    "10–15 días",
    "lorem ipsum",
    "Lorem ipsum",
    "LaTeX",
    "PDF +",
    "fuente editable",
    "editable source",
    "Reconquista, Santa Fe",
]
PRICE_PAGES = {
    "index.html",
    "documento.html",
    "contacto.html",
    "en/index.html",
    "en/document.html",
    "en/contact.html",
}
SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "javascript:", "data:")


class Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = ""
        self._in_title = False
        self.metas: list[dict] = []
        self.links: list[dict] = []
        self.anchors: list[dict] = []
        self.images: list[dict] = []
        self.scripts: list[dict] = []
        self.ids: set[str] = set()
        self.id_list: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        d = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag == "html":
            self.lang = d.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            self.metas.append(d)
        elif tag == "link":
            self.links.append(d)
        elif tag == "a":
            self.anchors.append(d)
        elif tag == "img":
            self.images.append(d)
        elif tag == "script" and d.get("src"):
            self.scripts.append(d)
        if d.get("id"):
            self.ids.add(d["id"])
            self.id_list.append(d["id"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def meta_value(parser: Collector, name: str) -> str | None:
    for m in parser.metas:
        if m.get("name", "").lower() == name.lower():
            return m.get("content", "")
    return None


def og_value(parser: Collector, prop: str) -> str | None:
    for m in parser.metas:
        if m.get("property", "").lower() == prop.lower():
            return m.get("content", "")
    return None


def rel_links(parser: Collector, rel: str) -> list[str]:
    out = []
    for link in parser.links:
        if rel in link.get("rel", "").lower().split():
            out.append(link.get("href", ""))
    return out


def hreflang_map(parser: Collector) -> dict[str, str]:
    out = {}
    for link in parser.links:
        if "alternate" in link.get("rel", "").lower().split() and link.get("hreflang"):
            out[link["hreflang"].lower()] = link.get("href", "")
    return out


def public_path(rel: str) -> str:
    if rel.endswith("index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def resolve(base: Path, href: str) -> Path | None:
    href = unquote(href.strip())
    if not href or href.startswith("#") or href.lower().startswith(SKIP_SCHEMES):
        return None
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href:
        return None
    if href.startswith("/"):
        target = base.parent.parent / href.lstrip("/") if base.parent.name == "en" else base.parent / href.lstrip("/")
    else:
        target = base.parent / href
    target = target.resolve()
    if target.is_dir():
        target = target / "index.html"
    return target


def check_page(path: Path, root: Path) -> list[str]:
    errors: list[str] = []
    raw = path.read_text(encoding="utf-8", errors="replace")
    parser = Collector()
    parser.feed(raw)

    rel = path.relative_to(root).as_posix()
    expected_lang = "en" if rel.startswith("en/") else "es"
    if parser.lang != expected_lang:
        errors.append(f"lang={parser.lang!r}, se esperaba {expected_lang!r}")

    title = " ".join(parser.title.split())
    if len(title) < 10:
        errors.append("title ausente o demasiado corto")

    desc = meta_value(parser, "description") or ""
    if len(desc.strip()) < 40:
        errors.append("meta description ausente o demasiado corta")

    canonical = rel_links(parser, "canonical")
    if not canonical:
        errors.append("falta link rel=canonical")
    else:
        for c in canonical:
            if SITE_HOST not in c:
                errors.append(f"canonical no usa {SITE_HOST}: {c}")

    if not rel_links(parser, "icon"):
        errors.append("falta favicon")

    for prop in ("og:type", "og:title", "og:description", "og:url", "og:image"):
        if not og_value(parser, prop):
            errors.append(f"falta {prop}")

    if path.name != "404.html":
        hl = hreflang_map(parser)
        for code in REQUIRED_HREFLANG:
            if code not in hl:
                errors.append(f"falta hreflang {code}")
        for code, href in hl.items():
            if SITE_HOST not in href:
                errors.append(f"hreflang {code} no usa {SITE_HOST}: {href}")

    for m in parser.metas:
        if m.get("name", "").lower() == "viewport" and "width=device-width" not in m.get("content", ""):
            errors.append("viewport no incluye width=device-width")

    for tag in ("img",):
        for img in parser.images:
            if "alt" not in img:
                errors.append(f"imagen sin alt: {img.get('src', '?')}")
            src = img.get("src", "")
            target = resolve(path, src)
            if target and not target.exists():
                errors.append(f"imagen inexistente: {src}")

    for a in parser.anchors:
        href = a.get("href", "")
        if href.startswith("#") and len(href) > 1 and href[1:] not in parser.ids:
            errors.append(f"ancla interna inexistente: {href}")
        target = resolve(path, href)
        if target and not target.exists():
            errors.append(f"enlace interno roto: {href}")

    for script in parser.scripts:
        target = resolve(path, script.get("src", ""))
        if target and not target.exists():
            errors.append(f"script inexistente: {script.get('src')}")

    for link in parser.links:
        href = link.get("href", "")
        if "stylesheet" in link.get("rel", "").lower().split():
            target = resolve(path, href)
            if target and not target.exists():
                errors.append(f"stylesheet inexistente: {href}")

    for value in re.findall(r'data-usd="([^"]*)"', raw):
        if not re.fullmatch(r"\d+(?:-\d+)?\+?", value):
            errors.append(f"data-usd inválido: {value}")

    if rel in PRICE_PAGES:
        slots = len(re.findall(r"data-price-ars", raw))
        if slots < 3:
            errors.append(f"precios en ARS insuficientes: {slots}")
    if "data-rate-note" not in raw:
        errors.append("sin nota de cotización (data-rate-note)")
    if "assets/js/rates.js" not in raw:
        errors.append("no carga assets/js/rates.js")

    lower = raw.lower()
    for banned in BANNED:
        if banned.lower() in lower:
            errors.append(f"cadena prohibida: {banned}")

    if re.search(r"\bTODO\b", raw):
        errors.append("marcador TODO sin resolver")

    if len(parser.id_list) != len(set(parser.id_list)):
        errors.append("ids duplicados")

    return [f"{rel}: {e}" for e in errors]


def public_html_files(root: Path) -> list[Path]:
    files = []
    for p in sorted(root.rglob("*.html")):
        rel = p.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        files.append(p)
    return files


def check_links(root: Path) -> list[str]:
    errors: list[str] = []
    for path in public_html_files(root):
        raw = path.read_text(encoding="utf-8", errors="replace")
        parser = Collector()
        parser.feed(raw)
        for a in parser.anchors:
            href = a.get("href", "")
            target = resolve(path, href)
            if target and not target.exists():
                errors.append(f"{path.relative_to(root)}: enlace roto -> {href}")
        for img in parser.images:
            target = resolve(path, img.get("src", ""))
            if target and not target.exists():
                errors.append(f"{path.relative_to(root)}: imagen rota -> {img.get('src')}")
    return errors


def check_parity(root: Path, allow_missing: bool) -> list[str]:
    errors: list[str] = []
    for es_rel, en_rel in PAIRS:
        es = root / es_rel
        en = root / en_rel
        if not es.exists() and not en.exists():
            if not allow_missing:
                errors.append(f"par ausente: {es_rel} / {en_rel}")
            continue
        if es.exists() != en.exists():
            if not allow_missing:
                errors.append(f"par incompleto: {es_rel}={'sí' if es.exists() else 'no'} / {en_rel}={'sí' if en.exists() else 'no'}")
            continue
        es_parser = Collector(); es_parser.feed(es.read_text(encoding="utf-8", errors="replace"))
        en_parser = Collector(); en_parser.feed(en.read_text(encoding="utf-8", errors="replace"))
        es_hl = hreflang_map(es_parser)
        en_hl = hreflang_map(en_parser)
        if "en" in es_hl and urlparse(es_hl["en"]).path != public_path(en_rel):
            errors.append(f"{es_rel}: hreflang en no apunta a {en_rel}")
        if "es-ar" in en_hl and urlparse(en_hl["es-ar"]).path != public_path(es_rel):
            errors.append(f"{en_rel}: hreflang es-AR no apunta a {es_rel}")
    return errors


def check_pdfs(root: Path) -> list[str]:
    errors: list[str] = []
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        return errors
    for pdf in sorted((root / "assets" / "docs").glob("*.pdf")):
        try:
            text = subprocess.check_output([pdftotext, str(pdf), "-"], text=True, errors="replace")
        except Exception as exc:  # pragma: no cover - tool failure
            errors.append(f"{pdf.name}: no se pudo leer ({exc})")
            continue
        if "ird.com.ar" in text.lower():
            errors.append(f"{pdf.name}: contiene ird.com.ar")
        if "pyme de ejemplo" not in text.lower() and "example" not in text.lower():
            errors.append(f"{pdf.name}: no parece una muestra ilustrativa")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="site", help="raíz del sitio a verificar")
    ap.add_argument("--allow-missing", action="store_true", help="no falla por páginas todavía no creadas")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"No existe: {root}")
        return 1

    errors: list[str] = []
    for path in public_html_files(root):
        errors.extend(check_page(path, root))
    errors.extend(check_links(root))
    errors.extend(check_parity(root, args.allow_missing))
    errors.extend(check_pdfs(root))

    if errors:
        print(f"FALLÓ: {len(errors)} problema(s)\n")
        for e in errors:
            print(f"  - {e}")
        return 1

    count = len(public_html_files(root))
    print(f"OK: {count} página(s) verificadas en {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
