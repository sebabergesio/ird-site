#!/usr/bin/env python3
"""Genera el sitio estático de IRD a partir de src/layout.html y src/pages/.

El sitio publicado es HTML plano. Este script es una herramienta de mantenimiento:
no se ejecuta en producción ni es necesario para navegar el sitio.

Uso (desde la raíz del proyecto):
    python tools/build_site.py
    python tools/build_site.py --only home
    python tools/build_site.py --allow-missing

El sitio publicado se escribe en site/.
"""

from __future__ import annotations

import argparse
import html
import posixpath
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
ROOT = PROJECT / "site"
SITE_URL = "https://ird.example"
EMAIL = "sebabergesio472@gmail.com"

PATHS = {
    "es": {
        "home": "index.html",
        "documento": "documento.html",
        "laboratorio": "laboratorio.html",
        "sobre-mi": "sobre-mi.html",
        "contacto": "contacto.html",
        "terminos": "terminos.html",
    },
    "en": {
        "home": "en/index.html",
        "documento": "en/document.html",
        "laboratorio": "en/lab.html",
        "sobre-mi": "en/about.html",
        "contacto": "en/contact.html",
        "terminos": "en/terms.html",
    },
}

NAV = {
    "es": [
        ("documento", "El documento"),
        ("laboratorio", "Laboratorio"),
        ("sobre-mi", "Sobre mí"),
        ("contacto", "Contacto"),
    ],
    "en": [
        ("documento", "The document"),
        ("laboratorio", "Lab"),
        ("sobre-mi", "About"),
        ("contacto", "Contact"),
    ],
}

COPY = {
    "es": {
        "brand_tag": "Ingeniería Rápida de Diseño",
        "cta": "Contame tu problema",
        "nav_label": "Principal",
        "menu_label": "Abrir menú",
        "skip": "Saltar al contenido",
        "home_aria": "IRD — Ingeniería Rápida de Diseño — Inicio",
        "footer_tagline": "Documentos técnicos de solución para problemas industriales y de proceso.",
        "location": "Avellaneda, Santa Fe, Argentina",
        "remote": "Trabajo remoto en todo el país y el exterior.",
        "nav_title": "Navegación",
        "contact_title": "Contacto",
        "legal_title": "Legal",
        "terms": "Términos y privacidad",
        "privacy": "Privacidad",
        "privacy_anchor": "privacidad",
        "sample": "Documento de muestra",
        "switch_label": "EN",
        "switch_full": "English",
        "og_locale": "es_AR",
        "og_locale_alt": "en_US",
    },
    "en": {
        "brand_tag": "Rapid Design Engineering",
        "cta": "Tell me what's not working",
        "nav_label": "Main",
        "menu_label": "Open menu",
        "skip": "Skip to content",
        "home_aria": "IRD — Rapid Design Engineering — Home",
        "footer_tagline": "Technical solution documents for industrial and process problems.",
        "location": "Avellaneda, Santa Fe, Argentina",
        "remote": "Remote work across Argentina and worldwide.",
        "nav_title": "Navigation",
        "contact_title": "Contact",
        "legal_title": "Legal",
        "terms": "Terms and privacy",
        "privacy": "Privacy",
        "privacy_anchor": "privacy",
        "sample": "Sample document",
        "switch_label": "ES",
        "switch_full": "Español",
        "og_locale": "en_US",
        "og_locale_alt": "es_AR",
    },
}


@dataclass(frozen=True)
class Page:
    key: str
    lang: str
    out: str
    title: str
    description: str
    nav: str
    og_image: str
    body_class: str = ""
    no_hreflang: bool = False
    robots: str = ""


PAGES = [
    Page(
        "home", "es", "index.html",
        "IRD — Documento técnico de solución | Sebastián Bergesio",
        "Analizo el problema, comparo alternativas y entrego un documento técnico de solución en PDF. Desde USD 1.200. Precios en USD y ARS al MEP del día.",
        "home", "assets/img/og-ird-es.png", "page-home",
    ),
    Page(
        "documento", "es", "documento.html",
        "El documento de solución: qué incluye y cuánto cuesta | IRD",
        "Qué incluye el documento de solución de IRD: 8 secciones, 3 alternativas comparadas, 15–25 días y entrega en PDF final. Desde USD 1.200, en USD y ARS.",
        "documento", "assets/img/og-ird-es.png", "page-documento",
    ),
    Page(
        "laboratorio", "es", "laboratorio.html",
        "Laboratorio: valorización de biomasa | IRD",
        "Investigación propia sobre valorización de biomasa: estado, hipótesis y próximos pasos. 45% de avance, revisión octubre 2026. Sin métricas inventadas.",
        "laboratorio", "assets/img/og-ird-es.png", "page-laboratorio",
    ),
    Page(
        "sobre-mi", "es", "sobre-mi.html",
        "Sobre mí: Sebastián Bergesio, UTN | IRD",
        "Sebastián Bergesio, estudiante de 3.º año de Ingeniería Electromecánica (UTN Reconquista). Documentación técnica, no ejecución ni firma de proyectos.",
        "sobre-mi", "assets/img/og-ird-es.png", "page-sobre-mi",
    ),
    Page(
        "contacto", "es", "contacto.html",
        "Contacto: contame tu problema | IRD",
        "Contame qué problema técnico tenés. Respondo en 24–48 horas hábiles con los siguientes pasos y un presupuesto dentro de 7 días.",
        "contacto", "assets/img/og-ird-es.png", "page-contacto",
    ),
    Page(
        "terminos", "es", "terminos.html",
        "Términos, pagos y privacidad | IRD",
        "Condiciones de contratación, pagos en USD y ARS al MEP del día, ajuste por IPC, plazos, propiedad intelectual y privacidad de IRD. Versión octubre 2026.",
        "terminos", "assets/img/og-ird-es.png", "page-terminos",
    ),
    Page(
        "home", "en", "en/index.html",
        "IRD — Technical solution document | Sebastián Bergesio",
        "I analyze the problem, compare alternatives and deliver a technical solution document as a PDF. From USD 1,200. Prices in USD and ARS at the day's MEP rate.",
        "home", "assets/img/og-ird-en.png", "page-home",
    ),
    Page(
        "documento", "en", "en/document.html",
        "The solution document: what it includes and what it costs | IRD",
        "What IRD's solution document includes: 8 sections, 3+ compared alternatives, 15–25 days, final PDF. From USD 1,200, in USD and ARS.",
        "documento", "assets/img/og-ird-en.png", "page-documento",
    ),
    Page(
        "laboratorio", "en", "en/lab.html",
        "Lab: biomass valorization research | IRD",
        "Independent research on biomass valorization: status, hypothesis and next steps. 45% complete, reviewed October 2026. No invented metrics.",
        "laboratorio", "assets/img/og-ird-en.png", "page-laboratorio",
    ),
    Page(
        "sobre-mi", "en", "en/about.html",
        "About Sebastián Bergesio, UTN | IRD",
        "Sebastián Bergesio, third-year Electromechanical Engineering student at UTN Reconquista. Technical documentation, not project execution or sign-off.",
        "sobre-mi", "assets/img/og-ird-en.png", "page-sobre-mi",
    ),
    Page(
        "contacto", "en", "en/contact.html",
        "Contact: tell me what's not working | IRD",
        "Tell me what technical problem you're facing. I reply within 24–48 business hours with next steps and a quote within 7 days.",
        "contacto", "assets/img/og-ird-en.png", "page-contacto",
    ),
    Page(
        "terminos", "en", "en/terms.html",
        "Terms, payment and privacy | IRD",
        "IRD's engagement terms, USD and ARS pricing at the day's MEP rate, IPC adjustment, deadlines, intellectual property and privacy. October 2026 version.",
        "terminos", "assets/img/og-ird-en.png", "page-terminos",
    ),
    Page(
        "404", "es", "404.html",
        "Página no encontrada | IRD",
        "La página que buscás no existe. Volvé al inicio, mirá el documento de solución o contame qué necesitás.",
        "", "assets/img/og-ird-es.png", "page-404", no_hreflang=True, robots="noindex",
    ),
]


def href(page: Page, target_out: str) -> str:
    start = posixpath.dirname(page.out) or "."
    return posixpath.relpath(target_out, start=start)


def asset_prefix(page: Page) -> str:
    parent = posixpath.dirname(page.out)
    if parent in ("", "."):
        return ""
    return "../" * len(parent.split("/"))


def public_url(out: str) -> str:
    if out == "index.html":
        return SITE_URL + "/"
    if out == "en/index.html":
        return SITE_URL + "/en/"
    return SITE_URL + "/" + out


def nav_links(page: Page) -> str:
    items = []
    for key, label in NAV[page.lang]:
        target = href(page, PATHS[page.lang][key])
        active = ' class="active" aria-current="page"' if page.nav == key else ""
        items.append(f'<a href="{target}"{active}>{label}</a>')
    return "\n          ".join(items)


def render_header(page: Page) -> str:
    c = COPY[page.lang]
    home = href(page, PATHS[page.lang]["home"])
    contact = href(page, PATHS[page.lang]["contacto"])
    other = "en" if page.lang == "es" else "es"
    switch_key = page.key if page.key in PATHS[other] else "home"
    switch_href = href(page, PATHS[other][switch_key])
    logo = asset_prefix(page) + "assets/img/logo-negro.svg"
    links = nav_links(page)
    return f'''<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{home}" aria-label="{html.escape(c['home_aria'])}">
      <img src="{logo}" alt="" width="44" height="44">
      <span class="brand-tag">{c['brand_tag']}</span>
    </a>
    <nav class="nav-desktop" aria-label="{c['nav_label']}">
      {links}
    </nav>
    <div class="header-actions">
      <a class="lang-switch" href="{switch_href}" hreflang="{other}" lang="{other}">{c['switch_label']}</a>
      <a class="btn btn-solid btn-sm" href="{contact}">{c['cta']}</a>
    </div>
    <details class="menu">
      <summary aria-label="{c['menu_label']}"><span class="menu-icon" aria-hidden="true"><span></span><span></span><span></span></span></summary>
      <div class="menu-panel">
        <nav class="menu-nav" aria-label="{c['nav_label']}">
          {links}
        </nav>
        <a class="btn btn-solid" href="{contact}">{c['cta']}</a>
        <a class="lang-switch lang-switch-mobile" href="{switch_href}" hreflang="{other}" lang="{other}">{c['switch_full']}</a>
      </div>
    </details>
  </div>
</header>'''


def render_footer(page: Page) -> str:
    c = COPY[page.lang]
    home = href(page, PATHS[page.lang]["home"])
    doc = href(page, PATHS[page.lang]["documento"])
    terms = href(page, PATHS[page.lang]["terminos"])
    other = "en" if page.lang == "es" else "es"
    switch_key = page.key if page.key in PATHS[other] else "home"
    switch_href = href(page, PATHS[other][switch_key])
    logo = asset_prefix(page) + "assets/img/logo-blanco.svg"
    nav_items = "\n        ".join(
        f'<a href="{href(page, PATHS[page.lang][key])}">{label}</a>'
        for key, label in NAV[page.lang]
    )
    return f'''<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <a href="{home}" aria-label="{html.escape(c['home_aria'])}"><img src="{logo}" alt="IRD" width="56" height="56"></a>
      <p>{c['footer_tagline']}</p>
      <p class="footer-loc mono">{c['location']}</p>
    </div>
    <div class="footer-col">
      <p class="footer-title mono">{c['nav_title']}</p>
      {nav_items}
    </div>
    <div class="footer-col">
      <p class="footer-title mono">{c['contact_title']}</p>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <p>{c['remote']}</p>
      <p class="footer-rate" data-rate-note aria-live="polite"></p>
    </div>
    <div class="footer-col">
      <p class="footer-title mono">{c['legal_title']}</p>
      <a href="{terms}">{c['terms']}</a>
      <a href="{terms}#{c['privacy_anchor']}">{c['privacy']}</a>
      <a class="lang-switch" href="{switch_href}" hreflang="{other}" lang="{other}">{c['switch_full']}</a>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>© <span data-year>2026</span> IRD · {c['brand_tag']}</span>
    <a href="{doc}">{c['sample']} →</a>
  </div>
</footer>'''


def render_page(page: Page) -> str:
    fragment_path = PROJECT / "src" / "pages" / f"{page.key}.{page.lang}.html"
    if not fragment_path.exists():
        raise FileNotFoundError(f"Falta el fragmento {fragment_path.relative_to(PROJECT)}")
    content = fragment_path.read_text(encoding="utf-8")
    c = COPY[page.lang]

    canonical = public_url(page.out)
    og_image = SITE_URL + "/" + page.og_image
    if page.no_hreflang:
        hreflang = ""
    else:
        alt_es = public_url(PATHS["es"][page.key])
        alt_en = public_url(PATHS["en"][page.key])
        hreflang = (
            f'<link rel="alternate" hreflang="es-AR" href="{alt_es}">\n'
            f'<link rel="alternate" hreflang="en" href="{alt_en}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{alt_es}">'
        )
    robots = f'<meta name="robots" content="{page.robots}">' if page.robots else ""

    layout = (PROJECT / "src" / "layout.html").read_text(encoding="utf-8")
    replacements = {
        "LANG": page.lang,
        "TITLE": html.escape(page.title, quote=True),
        "DESCRIPTION": html.escape(page.description, quote=True),
        "CANONICAL": html.escape(canonical, quote=True),
        "HREFLANG": hreflang,
        "ROBOTS": robots,
        "OG_LOCALE": c["og_locale"],
        "OG_LOCALE_ALT": c["og_locale_alt"],
        "OG_IMAGE": html.escape(og_image, quote=True),
        "OG_IMAGE_ALT": html.escape(page.title, quote=True),
        "ASSET_PREFIX": asset_prefix(page),
        "SKIP_LABEL": c["skip"],
        "BODY_CLASS": page.body_class,
        "HEADER": render_header(page),
        "CONTENT": content,
        "FOOTER": render_footer(page),
    }
    for key, value in replacements.items():
        layout = layout.replace("{{" + key + "}}", value)
    leftover = re.findall(r"\{\{[A-Z_]+\}\}", layout)
    if leftover:
        raise ValueError(f"Placeholders sin resolver en {page.out}: {sorted(set(leftover))}")
    return layout


def write_sitemap(pages: list[Page]) -> None:
    indexable = [p for p in pages if p.key != "404"]
    if not indexable:
        return
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    today = date.today().isoformat()
    for page in indexable:
        alt_es = public_url(PATHS["es"][page.key])
        alt_en = public_url(PATHS["en"][page.key])
        lines.extend([
            "  <url>",
            f"    <loc>{public_url(page.out)}</loc>",
            f"    <lastmod>{today}</lastmod>",
            f'    <xhtml:link rel="alternate" hreflang="es-AR" href="{alt_es}"/>',
            f'    <xhtml:link rel="alternate" hreflang="en" href="{alt_en}"/>',
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{alt_es}"/>',
            "  </url>",
        ])
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n",
        encoding="utf-8", newline="\n",
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="generar solo estas claves (separadas por coma)")
    ap.add_argument("--allow-missing", action="store_true", help="omitir fragmentos todavía no escritos")
    args = ap.parse_args()

    selected = PAGES
    if args.only:
        keys = {k.strip() for k in args.only.split(",") if k.strip()}
        selected = [p for p in PAGES if p.key in keys]

    built: list[Page] = []
    missing: list[str] = []
    for page in selected:
        try:
            output = render_page(page)
        except FileNotFoundError as exc:
            missing.append(str(exc))
            continue
        target = ROOT / page.out
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8", newline="\n")
        built.append(page)
        print(f"  + {page.out}")

    if missing:
        for item in missing:
            print(f"  ! {item}", file=sys.stderr)
        if not args.allow_missing:
            print(f"FALLÓ: faltan {len(missing)} fragmento(s)", file=sys.stderr)
            return 1

    existing = [p for p in PAGES if (PROJECT / "src" / "pages" / f"{p.key}.{p.lang}.html").exists()]
    write_sitemap(existing)
    print(f"OK: {len(built)} página(s) generadas; sitemap con {len([p for p in existing if p.key != '404'])} URL(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
