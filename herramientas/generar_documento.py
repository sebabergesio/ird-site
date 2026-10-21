#!/usr/bin/env python3
"""Genera un PDF de solución IRD a partir de un JSON y la Plantilla.tex oficial.

El script no reemplaza el diseño: toma `Recursos/Plantilla.tex`, completa los
campos `\\campoVacio{...}` en orden, arma la tabla de alternativas, copia el
logo (y las imágenes opcionales), y compila con pdflatex.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

IRD_ROOT = Path(__file__).resolve().parent.parent
PLANTILLA_POR_DEFECTO = IRD_ROOT / "Recursos" / "Plantilla.tex"
LOGO_POR_DEFECTO = IRD_ROOT / "Recursos" / "LogoNegro.png"


class ValidationError(Exception):
    """Los datos de entrada no cumplen el esquema."""


class TemplateError(Exception):
    """La plantilla no tiene la estructura esperada."""


class PdfError(Exception):
    """Falló la compilación o la generación del PDF."""


@dataclass(frozen=True)
class Campo:
    key: str
    label: str
    required: bool = True
    default: str = "No aplica."
    raw: bool = False


CAMPOS: tuple[Campo, ...] = (
    Campo("codigo", "Código de solución"),
    Campo("titulo", "Título de la solución"),
    Campo("cliente", "Cliente"),
    Campo("fecha", "Fecha"),
    Campo("version", "Versión"),
    Campo("resumen.problema", "Problema en 3 líneas"),
    Campo("resumen.solucion", "Solución en 3 líneas"),
    Campo("resumen.beneficio", "Beneficio esperado"),
    Campo("resumen.recursos", "Recursos necesarios para implementar"),
    Campo("problema.descripcion", "Descripción"),
    Campo("problema.causa_raiz", "Causa raíz (no el síntoma)"),
    Campo("problema.datos_respaldo", "Fuentes verificables"),
    Campo("problema.consecuencias", "Consecuencias"),
    Campo(
        "criterios_evaluacion",
        "Criterios de evaluación (costo, tiempo, complejidad, riesgo, normativa)",
    ),
    Campo("solucion.descripcion_tecnica", "Descripción"),
    Campo("solucion.criterios_diseno", "Parámetros y normativas aplicables"),
    Campo("solucion.condiciones_implementacion", "Qué se necesita / qué se debe evitar"),
    Campo(
        "solucion.diagramas",
        "Insertar diagramas, tablas o esquemas si aplica",
        required=False,
        raw=True,
    ),
    Campo(
        "resultado.beneficio_medible",
        "Beneficio medible (ahorro, reducción de tiempos, mejora de eficiencia)",
    ),
    Campo("resultado.supuestos", "Supuestos bajo los cuales se calculó"),
    Campo("licencia.tipo", "Tipo de licencia (uso, no venta)"),
    Campo("licencia.prohibicion", "Prohibición de reproducción y distribución"),
    Campo(
        "licencia.vigencia",
        "Vigencia de la solución (si aplica)",
        required=False,
    ),
    Campo("anexos.fuentes", "Fuentes"),
    Campo("anexos.normativas", "Normativas", required=False),
    Campo("anexos.glosario", "Glosario (si el cliente no es ingeniero)", required=False),
)

CAMPO_VACIO_RE = re.compile(r"\\campoVacio\{([^{}]*)\}")

# Se reemplaza carácter por carácter para no escapar dos veces las llaves que
# introduce el propio reemplazo.
_REEMPLAZOS_LATEX = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "$": r"\$",
    "&": r"\&",
    "#": r"\#",
    "%": r"\%",
    "_": r"\_",
    "^": r"\textasciicircum{}",
    "~": r"\textasciitilde{}",
    "–": "--",
    "—": "---",
    "“": "``",
    "”": "''",
    "‘": "`",
    "’": "'",
    "…": r"\ldots{}",
}


def latex_escape(text: str) -> str:
    """Escapa caracteres especiales de LaTeX en texto plano."""
    return "".join(_REEMPLAZOS_LATEX.get(char, char) for char in str(text))


def latex_inline(text: str) -> str:
    """Escapa un valor para usarlo dentro de una celda de tabla."""
    return latex_escape(re.sub(r"\s+", " ", str(text)).strip())


def latex_paragraphs(text: str) -> str:
    """Escapa texto y conserva párrafos separados por líneas en blanco."""
    normalizado = str(text).replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalizado:
        return ""
    parrafos = re.split(r"\n\s*\n", normalizado)
    return "\n\n".join(
        latex_escape(re.sub(r"\s*\n\s*", " ", parrafo).strip())
        for parrafo in parrafos
        if parrafo.strip()
    )


def _normalizar_etiqueta(texto: str) -> str:
    sin_acentos = unicodedata.normalize("NFKD", texto)
    sin_acentos = "".join(c for c in sin_acentos if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", sin_acentos).strip().lower()


def _get_nested(data: dict[str, Any], path: str, default: Any = None) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def _resolver_imagen(raw: str, base_dir: Path) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    for base in (base_dir, IRD_ROOT):
        candidate = base / path
        if candidate.exists():
            return candidate
    return base_dir / path


def _copiar_asset(origen: Path, destino_dir: Path, nombre: str | None = None) -> Path:
    if not origen.exists():
        raise ValidationError(f"No existe el archivo requerido: {origen}")
    destino = destino_dir / (nombre or origen.name)
    if origen.resolve() != destino.resolve():
        shutil.copy2(origen, destino)
    return destino


def _construir_diagramas(
    data: dict[str, Any], base_dir: Path, output_dir: Path
) -> str:
    solucion = data.get("solucion", {})
    if not isinstance(solucion, dict):
        raise ValidationError("El campo 'solucion' debe ser un objeto.")

    texto = str(solucion.get("diagramas", "") or "").strip()
    figuras: list[str] = []

    imagenes = solucion.get("imagenes", [])
    if imagenes is None:
        imagenes = []
    if not isinstance(imagenes, list):
        raise ValidationError("El campo 'solucion.imagenes' debe ser una lista.")

    for indice, imagen in enumerate(imagenes, 1):
        if not isinstance(imagen, dict):
            raise ValidationError(
                f"La imagen {indice} debe ser un objeto con 'ruta' y, opcionalmente, 'caption'."
            )
        raw = str(imagen.get("ruta", "") or "").strip()
        if not raw:
            raise ValidationError(f"Falta 'ruta' en la imagen {indice}.")
        origen = _resolver_imagen(raw, base_dir)
        if not origen.exists():
            raise ValidationError(
                f"No se encontró la imagen {indice}: {origen}. "
                "Usá una ruta absoluta o relativa al JSON."
            )
        extension = origen.suffix.lower()
        if extension not in {".png", ".jpg", ".jpeg", ".pdf"}:
            raise ValidationError(
                f"Formato de imagen no soportado: {origen.suffix}. Usá PNG, JPG o PDF."
            )

        nombre_destino = f"imagen_{indice}{extension}"
        _copiar_asset(origen, output_dir, nombre_destino)
        caption = str(imagen.get("caption", "") or "").strip()
        width = str(imagen.get("width", r"0.9\textwidth") or "").strip()
        if not re.fullmatch(r"(0\.\d+|1(\.0)?)\\textwidth", width):
            width = r"0.9\textwidth"

        figura = [
            r"\begin{figure}[h]",
            r"\centering",
            rf"\includegraphics[width={width}]{{{nombre_destino}}}",
        ]
        if caption:
            figura.append(rf"\caption{{{latex_escape(caption)}}}")
        figura.append(r"\end{figure}")
        figuras.append("\n".join(figura))

    etiqueta = "Insertar diagramas, tablas o esquemas si aplica"
    partes: list[str] = []
    if figuras and texto.lower() in {"no aplica.", "no aplica", "n/a"}:
        texto = ""
    texto_escapado = latex_paragraphs(texto) if texto else ""
    if texto_escapado:
        partes.append(f"\\campo{{{etiqueta}}}{{{texto_escapado}}}")
    elif figuras:
        partes.append(
            rf"\textbf{{\textcolor{{irdblack}}{{{etiqueta}:}}}}"
        )
    partes.extend(figuras)

    if partes:
        return "\n\n".join(partes)
    return f"\\campo{{{etiqueta}}}{{No aplica.}}"


def _recolectar_valores(
    data: dict[str, Any], base_dir: Path, output_dir: Path
) -> dict[str, str]:
    valores: dict[str, str] = {}
    for campo in CAMPOS:
        if campo.key == "solucion.diagramas":
            valores[campo.key] = _construir_diagramas(data, base_dir, output_dir)
            continue

        valor = _get_nested(data, campo.key)
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            if campo.required:
                raise ValidationError(f"Falta el campo obligatorio '{campo.key}'.")
            valores[campo.key] = campo.default
            continue
        if isinstance(valor, (dict, list)):
            raise ValidationError(f"El campo '{campo.key}' debe ser texto.")
        valores[campo.key] = str(valor)
    return valores


def _validar_alternativas(data: dict[str, Any]) -> list[dict[str, str]]:
    alternativas = data.get("alternativas")
    if not isinstance(alternativas, list):
        raise ValidationError("El campo 'alternativas' debe ser una lista.")
    if not 2 <= len(alternativas) <= 6:
        raise ValidationError(
            "El campo 'alternativas' debe tener entre 2 y 6 elementos."
        )

    limpias: list[dict[str, str]] = []
    for indice, alternativa in enumerate(alternativas, 1):
        if not isinstance(alternativa, dict):
            raise ValidationError(f"La alternativa {indice} debe ser un objeto.")
        for key in ("nombre", "costo", "tiempo", "riesgo", "motivo"):
            valor = alternativa.get(key)
            if valor is None or not str(valor).strip():
                raise ValidationError(
                    f"Falta '{key}' en la alternativa {indice}."
                )

        nombre = str(alternativa["nombre"]).strip()
        if not nombre.lower().startswith("alternativa"):
            nombre = f"Alternativa {nombre}"
        limpias.append(
            {
                "nombre": nombre,
                "costo": str(alternativa["costo"]),
                "tiempo": str(alternativa["tiempo"]),
                "riesgo": str(alternativa["riesgo"]),
                "motivo": str(alternativa["motivo"]),
            }
        )
    return limpias


def _completar_campos(plantilla: str, valores: dict[str, str]) -> str:
    matches = list(CAMPO_VACIO_RE.finditer(plantilla))
    if len(matches) != len(CAMPOS):
        raise TemplateError(
            f"La plantilla tiene {len(matches)} campos '\\campoVacio' y el generador "
            f"espera {len(CAMPOS)}. Actualizá el generador o la plantilla."
        )

    for match, campo in zip(matches, CAMPOS):
        if _normalizar_etiqueta(match.group(1)) != _normalizar_etiqueta(campo.label):
            raise TemplateError(
                "La plantilla cambió de orden o de etiqueta. "
                f"Se esperaba '{campo.label}' y se encontró '{match.group(1)}'."
            )

    partes: list[str] = []
    ultimo = 0
    for match, campo in zip(matches, CAMPOS):
        partes.append(plantilla[ultimo : match.start()])
        if campo.raw:
            # El bloque ya incluye su propio \campo y deja las figuras fuera
            # de cualquier argumento de macro (LaTeX no permite \par ahí).
            partes.append(valores[campo.key])
        else:
            contenido = latex_paragraphs(valores[campo.key])
            etiqueta = match.group(1)
            partes.append(f"\\campo{{{etiqueta}}}{{{contenido}}}")
        ultimo = match.end()
    partes.append(plantilla[ultimo:])
    return "".join(partes)


def _quitar_definicion_campo_vacio(tex: str) -> str:
    """Elimina la definición de \\campoVacio del .tex generado.

    Una vez completados todos los campos ya no se usa y evita que quede el
    texto "[completar]" en el archivo de salida.
    """
    patron = re.compile(r"^\\newcommand\{\\campoVacio\}.*(?:\n|$)", re.MULTILINE)
    return patron.sub("", tex)


def _reemplazar_alternativas(tex: str, alternativas: list[dict[str, str]]) -> str:
    inicio_tabla = tex.find(r"\begin{tabular}")
    if inicio_tabla == -1:
        raise TemplateError("No se encontró la tabla de alternativas en la plantilla.")
    fin_tabla = tex.find(r"\end{tabular}", inicio_tabla)
    if fin_tabla == -1:
        raise TemplateError("La tabla de alternativas no tiene '\\end{tabular}'.")
    midrule = tex.find(r"\midrule", inicio_tabla, fin_tabla)
    bottomrule = tex.find(r"\bottomrule", midrule, fin_tabla)
    if midrule == -1 or bottomrule == -1:
        raise TemplateError("No se encontró el cuerpo de la tabla de alternativas.")

    filas: list[str] = []
    for indice, alternativa in enumerate(alternativas):
        celdas = [
            alternativa["nombre"],
            alternativa["costo"],
            alternativa["tiempo"],
            alternativa["riesgo"],
            alternativa["motivo"],
        ]
        filas.append(" & ".join(latex_inline(celda) for celda in celdas) + r" \\")
        if indice < len(alternativas) - 1:
            filas.append(r"\addlinespace")

    cuerpo = "\\midrule\n" + "\n".join(filas) + "\n\\bottomrule"
    return tex[:midrule] + cuerpo + tex[bottomrule + len(r"\bottomrule") :]


def _encontrar_pdflatex() -> str:
    override = os.environ.get("PDFLATEX")
    if override and Path(override).exists():
        return override

    encontrado = shutil.which("pdflatex")
    if encontrado:
        return encontrado

    candidatos = [
        Path(r"G:\MiKTeX\miktex\bin\x64\pdflatex.exe"),
        Path(r"C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe"),
    ]
    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        candidatos.append(
            Path(local_appdata) / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64" / "pdflatex.exe"
        )
    for candidato in candidatos:
        if candidato.exists():
            return str(candidato)

    raise PdfError(
        "No se encontró pdflatex. Instalá MiKTeX o definí la variable PDFLATEX "
        "con la ruta al ejecutable."
    )


def _compilar_pdf(pdflatex: str, tex_path: Path, output_dir: Path) -> None:
    comando = [
        pdflatex,
        "-interaction=nonstopmode",
        "-halt-on-error",
        tex_path.name,
    ]
    for pasada in range(1, 4):
        proceso = subprocess.run(
            comando,
            cwd=output_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        log_path = tex_path.with_suffix(".log")
        log = (
            log_path.read_text(encoding="utf-8", errors="replace")
            if log_path.exists()
            else ""
        )
        if proceso.returncode != 0:
            detalle = log or proceso.stdout or proceso.stderr
            ultimas = "\n".join(detalle.splitlines()[-45:])
            raise PdfError(
                f"pdflatex falló en la pasada {pasada}.\n{ultimas}"
            )
        if "Rerun to get" not in log and "Rerun LaTeX" not in log:
            break

    pdf_path = tex_path.with_suffix(".pdf")
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise PdfError("pdflatex terminó pero no generó un PDF válido.")


def _limpiar_auxiliares(tex_path: Path) -> None:
    for extension in (".aux", ".log", ".out", ".toc"):
        auxiliar = tex_path.with_suffix(extension)
        if auxiliar.exists():
            auxiliar.unlink()


def generar_documento(
    input_path: str | Path,
    output_path: str | Path,
    plantilla_path: str | Path = PLANTILLA_POR_DEFECTO,
    logo_path: str | Path = LOGO_POR_DEFECTO,
    keep_aux: bool = False,
) -> tuple[Path, Path]:
    """Genera el PDF y devuelve (ruta_pdf, ruta_tex)."""
    entrada = Path(input_path).resolve()
    salida = Path(output_path).resolve()
    if not entrada.exists():
        raise ValidationError(f"No existe el JSON de entrada: {entrada}")
    if salida.suffix.lower() != ".pdf":
        salida = salida.with_suffix(".pdf")

    output_dir = salida.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        data = json.loads(entrada.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(
            f"JSON inválido en {entrada}: {exc.msg} "
            f"(línea {exc.lineno}, columna {exc.colno})"
        ) from exc
    if not isinstance(data, dict):
        raise ValidationError("El JSON de entrada debe ser un objeto.")

    plantilla = Path(plantilla_path)
    if not plantilla.exists():
        raise ValidationError(f"No existe la plantilla: {plantilla}")
    logo = Path(logo_path)
    _copiar_asset(logo, output_dir, "LogoNegro.png")

    valores = _recolectar_valores(data, entrada.parent, output_dir)
    tex = _completar_campos(plantilla.read_text(encoding="utf-8"), valores)
    tex = _quitar_definicion_campo_vacio(tex)
    tex = _reemplazar_alternativas(tex, _validar_alternativas(data))

    tex_path = salida.with_suffix(".tex")
    tex_path.write_text(tex, encoding="utf-8", newline="\n")

    pdflatex = _encontrar_pdflatex()
    _compilar_pdf(pdflatex, tex_path, output_dir)
    if not keep_aux:
        _limpiar_auxiliares(tex_path)

    if not salida.exists() or salida.stat().st_size == 0:
        raise PdfError(f"No se generó el PDF esperado: {salida}")
    return salida, tex_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Genera un PDF de solución IRD desde un JSON y Plantilla.tex."
    )
    parser.add_argument("--input", required=True, help="JSON con los datos del documento.")
    parser.add_argument("--output", required=True, help="Ruta del PDF de salida.")
    parser.add_argument(
        "--plantilla",
        default=str(PLANTILLA_POR_DEFECTO),
        help="Ruta a Plantilla.tex (por defecto, la oficial de IRD).",
    )
    parser.add_argument(
        "--logo",
        default=str(LOGO_POR_DEFECTO),
        help="Ruta al LogoNegro.png (por defecto, el oficial de IRD).",
    )
    parser.add_argument(
        "--keep-aux",
        action="store_true",
        help="Conserva .aux, .log, .out y .toc para depurar.",
    )
    args = parser.parse_args(argv)

    try:
        pdf, tex = generar_documento(
            input_path=args.input,
            output_path=args.output,
            plantilla_path=args.plantilla,
            logo_path=args.logo,
            keep_aux=args.keep_aux,
        )
    except (ValidationError, TemplateError, PdfError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"PDF generado: {pdf}")
    print(f"LaTeX generado: {tex}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
