# IRD — sitio y material de trabajo

Sitio público de **IRD — Ingeniería Rápida de Diseño** y todo lo necesario para
mantenerlo. Una sola carpeta, una sola raíz de git.

## Dónde está cada cosa

| Carpeta | Qué es | Se publica |
|---|---|---|
| `site/` | Sitio generado: HTML, CSS, JS, imágenes y PDFs de muestra. | **Sí** |
| `src/` | Fuentes de las páginas ES/EN, layout y plantillas de Open Graph. | No |
| `admin/` | Panel de administración del catálogo (a implementar). | No |
| `content/` | Datos del catálogo y del laboratorio (a definir). | No |
| `assets/` | Marca, plantilla LaTeX, logo y documentos de ejemplo. | No |
| `tools/` | Build, verificación, publicación y generador de PDF. | No |
| `docs/` | Especificación, planes, mockups y notas de agentes. | No |
| `archive/` | Sitio anterior y versiones viejas. | No |
| `var/` | Salidas descartables: `dist`, ZIP, QA, compilaciones. | No |

**Regla de oro:** se edita `src/`, se genera `site/` y se publica solo `site/`.
No se edita el HTML de `site/` a mano; el CSS y el JS sí viven en `site/assets/`.

## Comandos

Desde la raíz del proyecto:

```powershell
# Generar el sitio en site/
python tools/build_site.py

# Verificar el sitio generado
python tools/check_site.py

# Publicar: build + copia a var/dist + validación + ZIP opcional
powershell -ExecutionPolicy Bypass -File tools/publish.ps1
powershell -ExecutionPolicy Bypass -File tools/publish.ps1 -NoBuild
```

Vista previa local:

```powershell
python -m http.server 8000 --directory site
```

Luego abrir `http://localhost:8000/`.

## Documentos PDF

El generador toma un JSON y la plantilla oficial, y produce el PDF y el `.tex`:

```powershell
python tools/generar_documento.py `
  --input tools/ejemplo.json `
  --output var/documentos/ejemplo-SOL-001.pdf
```

Requiere MiKTeX con `pdflatex` disponible. El esquema del JSON y las reglas de
validación están en `tools/README.md`.

Pruebas:

```powershell
python -m unittest discover -s tools/tests -v
```

## Estado del proyecto

- El sitio actual es estático, bilingüe ES/EN y no está desplegado.
- Los precios se muestran en USD (ancla) y en ARS con cotización MEP en vivo
  (`site/assets/js/rates.js`, fuente: `dolarapi.com`). Si la consulta falla,
  queda visible el precio en USD y se avisa en pantalla.
- El dominio sigue como placeholder: `https://ird.example`.
- El catálogo de soluciones, el panel remoto, los pagos (Mercado Pago y PayPal)
  y la entrega automática están en etapa de diseño. No hay código de tienda
  todavía.

## Git

La raíz del repositorio es esta carpeta. `archive/` y `var/` no se versionan.
Antes de publicar, correr build y check; después commitear `src/` y `site/`
juntos para que el sitio generado y su fuente no se separen.
