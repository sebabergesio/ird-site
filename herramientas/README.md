# Generador de documentos IRD

Genera un PDF con el diseño oficial de IRD a partir de un JSON, usando
`Recursos/Plantilla.tex` y MiKTeX. No crea una plantilla nueva: completa los
campos `\campoVacio{...}` de la plantilla original, arma la tabla de
alternativas y compila con `pdflatex`.

## Requisitos

- Python 3.10 o superior.
- MiKTeX instalado y `pdflatex` disponible en el `PATH` (o definir `PDFLATEX`).
- `Recursos/Plantilla.tex` y `Recursos/LogoNegro.png`.

## Uso

```powershell
python "C:\Users\Sebas\Documents\OpenCode\IRD\herramientas\generar_documento.py" `
  --input "C:\Users\Sebas\Documents\OpenCode\IRD\herramientas\ejemplo.json" `
  --output "C:\Users\Sebas\Documents\OpenCode\IRD\documentos\ejemplo-SOL-001.pdf"
```

El script genera:

- `documentos/ejemplo-SOL-001.pdf`
- `documentos/ejemplo-SOL-001.tex` (para revisar o recompilar)
- `documentos/LogoNegro.png` (copia local para que el `.tex` sea autocontenido)

Opciones:

- `--plantilla RUTA`: usa otra plantilla con la misma estructura.
- `--logo RUTA`: usa otro logo.
- `--keep-aux`: conserva `.aux`, `.log`, `.out` y `.toc` para depurar.

## Esquema del JSON

Los campos con `*` son obligatorios. Los textos son texto plano: el script
escapa automáticamente `%`, `&`, `#`, `_`, etc.

```json
{
  "codigo": "SOL-001",
  "titulo": "Optimización de Procesos",
  "cliente": "PyME de ejemplo S.A.",
  "fecha": "2026-10-21",
  "version": "1.0",
  "resumen": {
    "problema": "Problema en tres líneas.",
    "solucion": "Solución en tres líneas.",
    "beneficio": "Beneficio esperado.",
    "recursos": "Recursos necesarios."
  },
  "problema": {
    "descripcion": "Descripción del problema.",
    "causa_raiz": "Causa raíz, no el síntoma.",
    "datos_respaldo": "Fuentes verificables.",
    "consecuencias": "Qué pasa si no se resuelve."
  },
  "criterios_evaluacion": "Costo, tiempo, complejidad, riesgo y normativa.",
  "alternativas": [
    {
      "nombre": "A",
      "costo": "USD 10.000",
      "tiempo": "8 semanas",
      "riesgo": "Bajo",
      "motivo": "Requiere inversión inicial."
    },
    {
      "nombre": "B",
      "costo": "USD 6.000",
      "tiempo": "12 semanas",
      "riesgo": "Medio",
      "motivo": "Mayor tiempo de implementación."
    }
  ],
  "solucion": {
    "descripcion_tecnica": "Descripción técnica.",
    "criterios_diseno": "Parámetros y normativas aplicables.",
    "condiciones_implementacion": "Qué se necesita y qué se debe evitar.",
    "diagramas": "Texto opcional para la sección de esquemas.",
    "imagenes": [
      {
        "ruta": "C:/ruta/al/esquema.png",
        "caption": "Esquema del proceso",
        "width": "0.9\\textwidth"
      }
    ]
  },
  "resultado": {
    "beneficio_medible": "Beneficio medible.",
    "supuestos": "Supuestos de cálculo."
  },
  "licencia": {
    "tipo": "Licencia de uso.",
    "prohibicion": "No se permite la reventa.",
    "vigencia": "12 meses."
  },
  "anexos": {
    "fuentes": "Fuentes consultadas.",
    "normativas": "Normativas citadas.",
    "glosario": "Glosario técnico."
  }
}
```

Reglas de validación:

- `alternativas` debe tener entre 2 y 6 elementos.
- Cada alternativa necesita `nombre`, `costo`, `tiempo`, `riesgo` y `motivo`.
- `solucion.imagenes` es opcional. Las rutas relativas se buscan desde la
  carpeta del JSON y desde la raíz de IRD.
- Si un campo opcional queda vacío, se escribe `No aplica.`.

## Cómo funciona

1. Lee el JSON y valida los campos.
2. Copia el logo y las imágenes a la carpeta de salida.
3. Reemplaza los 26 `\campoVacio{...}` de `Plantilla.tex` por
   `\campo{...}{...}`, en el orden de la plantilla.
4. Reemplaza las filas de ejemplo de la tabla de alternativas.
5. Compila dos o tres veces con `pdflatex` para resolver el índice.
6. Limpia los auxiliares y deja el `.pdf` y el `.tex`.

Si se modifica `Plantilla.tex`, hay que actualizar la lista `CAMPOS` de
`generar_documento.py` para que las etiquetas sigan coincidiendo.

## Pruebas

```powershell
python -m unittest discover -s "C:\Users\Sebas\Documents\OpenCode\IRD\herramientas\tests" -v
```

Las pruebas generan un PDF real y verifican que no quede `[completar]`, que los
caracteres especiales estén escapados y que la tabla de alternativas se arme.
