import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERRAMIENTAS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERRAMIENTAS))

try:
    import generar_documento as gd
except ImportError:
    gd = None


def datos_ejemplo():
    return {
        "codigo": "SOL-001",
        "titulo": "Optimización de Procesos",
        "cliente": "PyME de ejemplo S.A.",
        "fecha": "2026-10-21",
        "version": "1.0",
        "resumen": {
            "problema": "La línea de producción pierde tiempo por cuellos de botella.",
            "solucion": "Rediseño del flujo y balanceo de estaciones.",
            "beneficio": "Reducción estimada del 20% en tiempos de ciclo.",
            "recursos": "Dos semanas de relevamiento y un responsable de producción.",
        },
        "problema": {
            "descripcion": "El proceso actual tiene esperas entre estaciones y retrabajo.",
            "causa_raiz": "Falta de balanceo y de estándares de trabajo.",
            "datos_respaldo": "Registros de producción de los últimos tres meses.",
            "consecuencias": "Mayor costo unitario y entregas demoradas.",
        },
        "criterios_evaluacion": "Costo, tiempo, complejidad, riesgo y normativa aplicable.",
        "alternativas": [
            {
                "nombre": "A",
                "costo": "USD 10.000",
                "tiempo": "8 semanas",
                "riesgo": "Bajo",
                "motivo": "Requiere inversión inicial.",
            },
            {
                "nombre": "B",
                "costo": "USD 6.000",
                "tiempo": "12 semanas",
                "riesgo": "Medio",
                "motivo": "Mayor tiempo de implementación.",
            },
        ],
        "solucion": {
            "descripcion_tecnica": "Texto con 50% & #1 _x para probar el escapado.",
            "criterios_diseno": "Balanceo de líneas y análisis de tiempos.",
            "condiciones_implementacion": "No detener la producción durante el relevamiento.",
            "diagramas": "No aplica.",
        },
        "resultado": {
            "beneficio_medible": "Reducción del 20% en tiempos de ciclo.",
            "supuestos": "Demanda estable y disponibilidad del personal.",
        },
        "licencia": {
            "tipo": "Licencia de uso.",
            "prohibicion": "No se permite la reventa del documento.",
            "vigencia": "12 meses.",
        },
        "anexos": {
            "fuentes": "Registros internos del cliente.",
            "normativas": "No aplica.",
            "glosario": "Tiempo de ciclo: tiempo total de una unidad.",
        },
    }


class TestGeneradorDocumento(unittest.TestCase):
    def test_escapea_caracteres_especiales(self):
        self.assertIsNotNone(gd, "Falta implementar generar_documento.py")
        self.assertEqual(
            gd.latex_escape("50% & #1 _x"),
            r"50\% \& \#1 \_x",
        )

    def test_genera_pdf_con_plantilla_ird(self):
        self.assertIsNotNone(gd, "Falta implementar generar_documento.py")
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            entrada = tmp / "sol-001.json"
            salida = tmp / "sol-001.pdf"
            entrada.write_text(
                json.dumps(datos_ejemplo(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            proc = subprocess.run(
                [
                    sys.executable,
                    str(HERRAMIENTAS / "generar_documento.py"),
                    "--input",
                    str(entrada),
                    "--output",
                    str(salida),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(
                proc.returncode,
                0,
                msg=f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}",
            )
            self.assertTrue(salida.exists(), "No se generó el PDF")
            self.assertGreater(salida.stat().st_size, 10_000)

            tex = salida.with_suffix(".tex")
            self.assertTrue(tex.exists(), "No se generó el .tex")
            contenido = tex.read_text(encoding="utf-8")
            self.assertNotIn(r"\campoVacio", contenido)
            self.assertIn("Optimización de Procesos", contenido)
            self.assertIn(r"50\% \& \#1 \_x", contenido)
            self.assertIn("Alternativa A", contenido)
            self.assertIn("Alternativa B", contenido)
            self.assertNotIn("[completar]", contenido)

            pdftotext = shutil.which("pdftotext")
            if pdftotext:
                texto = subprocess.run(
                    [pdftotext, str(salida), "-"],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                ).stdout
                texto_plano = " ".join(texto.split())
                self.assertIn("Optimizaci", texto_plano)
                self.assertRegex(texto_plano, r"50\s*%")
                self.assertNotIn("[completar]", texto_plano)

    def test_incluye_imagenes_opcionales(self):
        self.assertIsNotNone(gd, "Falta implementar generar_documento.py")
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            datos = datos_ejemplo()
            datos["solucion"]["imagenes"] = [
                {
                    "ruta": str(
                        HERRAMIENTAS.parent / "assets" / "brand" / "LogoNegro.png"
                    ),
                    "caption": "Logo IRD",
                    "width": r"0.2\textwidth",
                }
            ]
            entrada = tmp / "con-imagen.json"
            salida = tmp / "con-imagen.pdf"
            entrada.write_text(
                json.dumps(datos, ensure_ascii=False), encoding="utf-8"
            )

            proc = subprocess.run(
                [
                    sys.executable,
                    str(HERRAMIENTAS / "generar_documento.py"),
                    "--input",
                    str(entrada),
                    "--output",
                    str(salida),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(
                proc.returncode,
                0,
                msg=f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}",
            )
            self.assertTrue((tmp / "imagen_1.png").exists())
            tex = salida.with_suffix(".tex").read_text(encoding="utf-8")
            self.assertIn(
                r"\includegraphics[width=0.2\textwidth]{imagen_1.png}", tex
            )
            self.assertIn(r"\caption{Logo IRD}", tex)
            self.assertNotIn(
                r"\campo{Insertar diagramas, tablas o esquemas si aplica}{No aplica.}",
                tex,
            )
            self.assertTrue(salida.exists())

    def test_falla_si_falta_campo_obligatorio(self):
        self.assertIsNotNone(gd, "Falta implementar generar_documento.py")
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            datos = datos_ejemplo()
            del datos["titulo"]
            entrada = tmp / "incompleto.json"
            salida = tmp / "incompleto.pdf"
            entrada.write_text(
                json.dumps(datos, ensure_ascii=False), encoding="utf-8"
            )

            proc = subprocess.run(
                [
                    sys.executable,
                    str(HERRAMIENTAS / "generar_documento.py"),
                    "--input",
                    str(entrada),
                    "--output",
                    str(salida),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("titulo", (proc.stdout + proc.stderr).lower())
            self.assertFalse(salida.exists())

    def test_falla_con_menos_de_dos_alternativas(self):
        self.assertIsNotNone(gd, "Falta implementar generar_documento.py")
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            datos = datos_ejemplo()
            datos["alternativas"] = datos["alternativas"][:1]
            entrada = tmp / "una-alternativa.json"
            salida = tmp / "una-alternativa.pdf"
            entrada.write_text(
                json.dumps(datos, ensure_ascii=False), encoding="utf-8"
            )

            proc = subprocess.run(
                [
                    sys.executable,
                    str(HERRAMIENTAS / "generar_documento.py"),
                    "--input",
                    str(entrada),
                    "--output",
                    str(salida),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("alternativas", (proc.stdout + proc.stderr).lower())
            self.assertFalse(salida.exists())


if __name__ == "__main__":
    unittest.main()
