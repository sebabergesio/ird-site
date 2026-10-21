# Reconstrucción del sitio de IRD — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reemplazar el sitio actual de IRD por un sitio estático bilingüe (ES/EN) que venda un documento técnico, muestre una muestra real y lleve a una consulta.

**Architecture:** HTML estático en la raíz para español y en `/en/` para inglés. Un CSS y un JS compartidos en `assets/`. Sin framework ni build obligatorio. El sitio viejo se archiva en `_legacy/` y no se publica. La publicación se arma copiando solo los archivos públicos a `dist/`.

**Tech Stack:** HTML5, CSS3 (custom properties, grid, `clamp`), JavaScript vanilla, PowerShell para verificación y publicación, LaTeX/MiKTeX para las muestras PDF, `pdftoppm` para previews.

**Spec:** `docs/superpowers/specs/2026-10-21-ird-website-design.md`

## Global Constraints

- Español en la raíz; inglés en `/en/`. Mismos contenidos y mismas secciones en ambos idiomas.
- No inventar casos, clientes, testimonios, métricas ni fechas. El laboratorio es investigación propia y se rotula como tal.
- No afirmar que IRD firma proyectos, ejecuta obra o hace prototipos. La documentación se entrega para validar y firmar con un profesional matriculado.
- Precios visibles: consulta USD 80; diagnóstico USD 450–500; documento completo USD 1.200–1.400; complejo desde USD 3.000; acompañamiento USD 300/mes.
- Moneda: precios en USD; cobro en ARS al MEP del día + 5%; presupuesto válido 7 días; saldos impagos ajustados por IPC.
- Correo funcional: `sebabergesio472@gmail.com`. El correo profesional queda pendiente hasta definir dominio.
- **No usar `ird.com.ar`**: está registrado por otra empresa. Usar `https://ird.example` como placeholder de canonical/sitemap hasta definir el dominio.
- No prometer medios de pago internacionales no configurados. Texto: "Para clientes del exterior, coordinamos el medio de pago al confirmar el proyecto."
- Todas las páginas: `lang`, title único, meta description única, canonical, hreflang `es-AR`/`en`/`x-default`, OG/Twitter, favicon, CSS y JS compartidos.
- Sin `href="#"`, sin "lorem", sin "TBD", sin "TODO" en el HTML público.
- Accesibilidad AA, foco visible, navegación por teclado, `prefers-reduced-motion`.
- El sitio debe funcionar sin JavaScript para leer y navegar; el formulario tiene fallback `mailto:`.
- Archivos viejos: mover a `_legacy/`; no borrar hasta terminar la verificación.

## Review Focus

1. **Links relativos en `/en/`**: cada `../assets/...`, `../index.html` y `../documento.html` debe resolver; un error rompe CSS, logos o el cambio de idioma.
2. **Pares bilingües**: cada página ES debe tener su equivalente EN y cada EN su equivalente ES; canonical y hreflang deben apuntar al par correcto.
3. **Contenido viejo**: no debe quedar `ird.com.ar`, precios viejos (`45.000`), "catálogo", "asistente" ni promesas de ejecución/firma.
4. **Mobile 320–390px**: la ficha de 8 filas, la hoja A4, las tablas de precios y el menú no deben generar scroll horizontal.
5. **Formulario sin JS o sin cliente de correo**: debe mostrar el email visible y un mensaje claro; no debe perder el texto escrito.

---

## File Structure

```
IRD/
  index.html                 Home ES
  documento.html             El documento ES
  laboratorio.html           Laboratorio ES
  sobre-mi.html              Sobre mí ES
  contacto.html              Contacto ES
  terminos.html              Términos y privacidad ES
  404.html                   404 bilingüe
  en/
    index.html               Home EN
    document.html            The document EN
    lab.html                 Lab EN
    about.html               About EN
    contact.html             Contact EN
    terms.html               Terms & privacy EN
  assets/
    css/style.css
    js/site.js
    img/logo-negro.svg
    img/logo-blanco.svg
    img/favicon.svg
    img/og-ird-es.png
    img/og-ird-en.png
    img/muestra-p1.jpg
    img/muestra-p2.jpg
    img/muestra-p3.jpg
    img/muestra-en-p1.jpg
    img/muestra-en-p2.jpg
    img/muestra-en-p3.jpg
    docs/muestra-SOL-001.pdf
    docs/muestra-SOL-001-en.pdf
  robots.txt
  sitemap.xml
  README.md
  tools/
    check_site.ps1
    publish.ps1
    og-es.html
    og-en.html
  _legacy/                   Sitio viejo, no se publica
  documentos/                Fuente de las muestras, no se publica
  Recursos/                  Logos y plantilla, no se publica
  herramientas/              Generador de documentos, no se publica
  docs/                      Diseño, plan, documentación, no se publica
```

**Clases CSS compartidas:** `.wrap`, `.site-header`, `.header-inner`, `.brand`, `.brand-tag`, `.nav-desktop`, `.nav-link`, `.header-actions`, `.lang`, `.menu`, `.menu-panel`, `.btn`, `.btn-solid`, `.btn-ghost`, `.btn-text`, `.eyebrow`, `.lead`, `.hero`, `.hero-grid`, `.hero-copy`, `.hero-visual`, `.spec`, `.spec-head`, `.spec-grid`, `.spec-row`, `.sheet`, `.sheet-top`, `.sheet-title`, `.sheet-sub`, `.sheet-k`, `.stamp`, `.section`, `.section-head`, `.section-index`, `.steps`, `.step`, `.step-num`, `.split`, `.panel`, `.checklist`, `.doc-preview`, `.doc-pages`, `.page-img`, `.price-grid`, `.price-card`, `.price-card.featured`, `.price`, `.price-note`, `.faq`, `.faq-item`, `.cta-band`, `.site-footer`, `.footer-grid`, `.footer-bottom`, `.page-hero`, `.band`, `.band-item`, `.callout`, `.status`, `.progress`, `.form`, `.field`, `.field-row`, `.monogram`, `.table-wrap`, `.sr-only`, `.skip-link`, `.reveal`.

**Interfaz de `site.js`:** cierra `<details class="menu">` al hacer clic en un link; revela `.reveal` con `IntersectionObserver`; actualiza `#year`; intercepta `#contact-form` y arma un `mailto:` con los campos; copia el email en `[data-copy]`. Sin dependencias.

---

### Task 1: Archivar el sitio viejo, crear estructura y checker

**Files:**
- Create: `_legacy/README.md`, `assets/css/`, `assets/js/`, `assets/img/`, `assets/docs/`, `en/`, `tools/`
- Move: `index.html`, `style.css`, `data.js`, `soluciones.html`, `producto.html`, `asistente.html`, `admin.html`, `terminos.html`, `404.html`, `Problemas/problema-001.html` → `_legacy/`
- Create: `tools/check_site.ps1`

**Interfaces:**
- Produces: `tools/check_site.ps1` que devuelve exit code 0 si todas las páginas públicas cumplen las reglas y 1 si hay errores.

- [ ] **Step 1: Crear carpetas y archivar**

```powershell
New-Item -ItemType Directory -Force _legacy, assets/css, assets/js, assets/img, assets/docs, en, tools | Out-Null
Move-Item index.html, style.css, data.js, soluciones.html, producto.html, asistente.html, admin.html, terminos.html, 404.html _legacy/
New-Item -ItemType Directory -Force _legacy/Problemas | Out-Null
Move-Item Problemas/problema-001.html _legacy/Problemas/
```

- [ ] **Step 2: Copiar logos y favicon**

Copiar `Recursos/Logo-Negro.svg` y `Recursos/Logo-Blanco.svg` a `assets/img/`. Copiar `Logo-Negro.svg` como `assets/img/favicon.svg`.

- [ ] **Step 3: Escribir `_legacy/README.md`**

Debe decir: "Sitio anterior de IRD, archivado el 2026-10-21. No se publica. Se conserva como referencia hasta que el sitio nuevo esté verificado."

- [ ] **Step 4: Escribir `tools/check_site.ps1`**

El script debe comprobar, para cada HTML público (`index.html`, `documento.html`, `laboratorio.html`, `sobre-mi.html`, `contacto.html`, `terminos.html`, `404.html`, `en/*.html`):

- `<html lang="es"` o `lang="en"`.
- Un solo `<h1>`.
- `<title>` no vacío y único.
- `meta name="description"` no vacía y única.
- `rel="canonical"`.
- `hreflang="es-AR"`, `hreflang="en"`, `hreflang="x-default"` (el 404 puede ser la excepción documentada).
- `assets/css/style.css` y `assets/js/site.js` (con `../` en `/en/`).
- Ningún `ird.com.ar`, `45.000`, `lorem`, `TBD`, `TODO`, `href="#"`.
- Todos los `href`/`src` locales existen (ignorar `mailto:`, `http`, `https`, `#`, `data:`).
- Cada página ES tiene par EN y viceversa (excepto 404).
- `robots.txt` y `sitemap.xml` existen.
- Los JSON-LD parsean con `ConvertFrom-Json`.
- Las imágenes OG miden 1200×630 si existen.

- [ ] **Step 5: Ejecutar el checker y confirmar que falla**

Run: `powershell -ExecutionPolicy Bypass -File tools/check_site.ps1`
Expected: FAIL con "faltan páginas" (todavía no existen).

---

### Task 2: Muestras PDF y previews

**Files:**
- Modify: `documentos/ejemplo-SOL-001.tex` (quitar `ird.com.ar`, marcar muestra)
- Modify: `Recursos/Plantilla.tex` (quitar `ird.com.ar`)
- Create: `documentos/ejemplo-SOL-001-en.tex`
- Create: `assets/docs/muestra-SOL-001.pdf`, `assets/docs/muestra-SOL-001-en.pdf`
- Create: `assets/img/muestra-p1.jpg`, `muestra-p2.jpg`, `muestra-p3.jpg`, `muestra-en-p1.jpg`, `muestra-en-p2.jpg`, `muestra-en-p3.jpg`

**Interfaces:**
- Produces: dos PDFs de 5 páginas y seis JPEGs de página completa para las previews.

- [ ] **Step 1: Corregir la portada y el pie de la muestra ES**

En `documentos/ejemplo-SOL-001.tex`, reemplazar `sebabergesio472@gmail.com · ird.com.ar` por `sebabergesio472@gmail.com`. En el pie, cambiar `Documento confidencial` por `Documento de muestra · Contenido ilustrativo`. Agregar bajo el título de portada: `DOCUMENTO DE MUESTRA · CONTENIDO ILUSTRATIVO`.

En `Recursos/Plantilla.tex`, reemplazar `sebabergesio472@gmail.com · ird.com.ar` por `sebabergesio472@gmail.com` (la plantilla oficial conserva su pie de confidencialidad).

- [ ] **Step 2: Compilar la muestra ES dos veces**

```powershell
cd documentos
pdflatex -interaction=nonstopmode ejemplo-SOL-001.tex
pdflatex -interaction=nonstopmode ejemplo-SOL-001.tex
Copy-Item ejemplo-SOL-001.pdf ../assets/docs/muestra-SOL-001.pdf -Force
```

Expected: PDF de 5 páginas, sin `ird.com.ar`, con el rótulo de muestra.

- [ ] **Step 3: Crear la muestra EN**

Copiar `documentos/ejemplo-SOL-001.tex` a `documentos/ejemplo-SOL-001-en.tex`. Cambiar `\usepackage[spanish,es-noshorthands]{babel}` por `\usepackage[english]{babel}`. Traducir portada, encabezados, campos, tabla, límites, licencia y anexos al inglés. Mantener código SOL-001, datos ilustrativos y estructura de 8 secciones. Título de portada: `SOLUTION DOCUMENT`; subtítulo: `SAMPLE DOCUMENT · ILLUSTRATIVE CONTENT`; cliente: `Sample Company`.

- [ ] **Step 4: Compilar la muestra EN dos veces**

```powershell
cd documentos
pdflatex -interaction=nonstopmode ejemplo-SOL-001-en.tex
pdflatex -interaction=nonstopmode ejemplo-SOL-001-en.tex
Copy-Item ejemplo-SOL-001-en.pdf ../assets/docs/muestra-SOL-001-en.pdf -Force
```

Expected: PDF de 5 páginas en inglés, sin `ird.com.ar`.

- [ ] **Step 5: Renderizar previews**

```powershell
pdftoppm -jpeg -jpegopt quality=82 -scale-to 900 -f 1 -l 1 -singlefile assets/docs/muestra-SOL-001.pdf assets/img/muestra-p1
pdftoppm -jpeg -jpegopt quality=82 -scale-to 900 -f 3 -l 3 -singlefile assets/docs/muestra-SOL-001.pdf assets/img/muestra-p2
pdftoppm -jpeg -jpegopt quality=82 -scale-to 900 -f 5 -l 5 -singlefile assets/docs/muestra-SOL-001.pdf assets/img/muestra-p3
pdftoppm -jpeg -jpegopt quality=82 -scale-to 900 -f 1 -l 1 -singlefile assets/docs/muestra-SOL-001-en.pdf assets/img/muestra-en-p1
pdftoppm -jpeg -jpegopt quality=82 -scale-to 900 -f 3 -l 3 -singlefile assets/docs/muestra-SOL-001-en.pdf assets/img/muestra-en-p2
pdftoppm -jpeg -jpegopt quality=82 -scale-to 900 -f 5 -l 5 -singlefile assets/docs/muestra-SOL-001-en.pdf assets/img/muestra-en-p3
```

- [ ] **Step 6: Verificar visualmente**

Abrir cada JPEG con `read` y confirmar que se lee la portada, el resumen y la tabla de alternativas; que no aparece `ird.com.ar`; que el rótulo de muestra es visible. Confirmar que cada archivo pesa menos de 200 KB.

---

### Task 3: CSS base y JavaScript compartido

**Files:**
- Create: `assets/css/style.css`
- Create: `assets/js/site.js`

**Interfaces:**
- Produces: tokens `--paper #F1F0EA`, `--ink #111417`, `--muted #5C6166`, `--line`, `--teal #0B6B6B`, `--accent #C2410C`, `--accent-bright #D9480F`; clases listadas arriba; `site.js` con las cuatro funciones.

- [ ] **Step 1: Escribir los tokens, reset y tipografía**

Incluir `@import` no; usar `<link>` de Google Fonts en cada página. Definir `box-sizing`, `margin:0`, `body` con papel y grilla de dos niveles, `::selection`, `:focus-visible` teal de 2px, `.wrap` max-width 1180px, `.mono`/`.eyebrow`, `.sr-only`, `.skip-link`.

- [ ] **Step 2: Escribir header, nav, menú `<details>` y footer**

Desktop: logo + nav + idioma + CTA. Mobile (`max-width: 900px`): ocultar `.nav-desktop` y `.nav-cta`; mostrar `.menu`. El panel del menú es absoluto bajo el header, fondo papel, borde, links grandes y CTA. `<summary>` sin marcador nativo. Footer de 4 columnas en desktop y stack en móvil.

- [ ] **Step 3: Escribir hero, ficha, hoja A4, secciones y componentes**

Incluir `.hero-grid` 1.15fr/0.85fr; `.spec` con borde 1px y `.spec-grid` de 2 columnas; `.sheet` blanca con sombra desplazada y tabla mono; `.section` con aire; `.steps` de 4 columnas; `.split` de 2; `.price-grid` de 3; `.faq` con `<details>`; `.cta-band`; `.table-wrap`; `.form`; `.band`; `.page-hero`; `.doc-pages`; `.callout`; `.status`; `.progress`; `.monogram`.

- [ ] **Step 4: Escribir responsive y motion**

Breakpoints 900px y 600px. En 900px: hero 1 columna, spec 1 columna, steps 2, price grid 1, footer 2. En 600px: todo 1 columna, tipografía más chica, sheet con padding reducido, tabla de la hoja con fuente 8px, `.doc-pages` en carrusel horizontal con `scroll-snap`. `@media (prefers-reduced-motion: reduce)` desactiva transiciones y reveal. Sin overflow horizontal.

- [ ] **Step 5: Escribir `assets/js/site.js`**

```js
(() => {
  const menu = document.querySelector('.menu');
  if (menu) menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => menu.removeAttribute('open')));
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const io = new IntersectionObserver(entries => entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); } }), { threshold: 0.12 });
    reveals.forEach(el => io.observe(el));
  } else reveals.forEach(el => el.classList.add('is-visible'));
  const form = document.getElementById('contact-form');
  if (form) form.addEventListener('submit', e => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    if (data.get('website')) return;
    const body = [...data.entries()].filter(([k]) => k !== 'website').map(([k, v]) => `${k}: ${v}`).join('\n');
    const mailto = `mailto:sebabergesio472@gmail.com?subject=${encodeURIComponent('Consulta desde el sitio de IRD')}&body=${encodeURIComponent(body)}`;
    window.location.href = mailto;
    const status = document.getElementById('form-status');
    if (status) { status.hidden = false; status.textContent = 'Se abrió tu cliente de correo. Si no pasó nada, escribime a sebabergesio472@gmail.com.'; }
  });
  document.querySelectorAll('[data-copy]').forEach(btn => btn.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(btn.dataset.copy); btn.textContent = 'Copiado'; } catch { window.location.href = `mailto:${btn.dataset.copy}`; }
  }));
})();
```

- [ ] **Step 6: Verificar sintaxis y carga**

Crear una página temporal `tools/_preview.html` con el header, un hero y el footer. Abrir con `browser.preview`, revisar consola si está disponible y sacar screenshot desktop/mobile. Eliminar `tools/_preview.html` al terminar.

---

### Task 4: Home en español

**Files:**
- Create: `index.html`

**Interfaces:**
- Consumes: `assets/css/style.css`, `assets/js/site.js`, `assets/img/*`, `assets/docs/muestra-SOL-001.pdf`.
- Produces: la home que enlaza a `documento.html`, `laboratorio.html`, `sobre-mi.html`, `contacto.html`, `en/index.html`.

- [ ] **Step 1: Escribir el `<head>`**

`lang="es"`, title `IRD · Documentación técnica para resolver problemas`, description de 150–160 caracteres, canonical `https://ird.example/`, hreflang `es-AR`/`en`/`x-default`, OG con `assets/img/og-ird-es.png` (se crea en Task 9; si todavía no existe, dejar la ruta y el checker la validará al final), Twitter card, favicon, Google Fonts Inter + IBM Plex Mono, CSS.

- [ ] **Step 2: Escribir header y hero**

Header con nav y CTA. Hero: eyebrow "Estudio técnico · Reconquista, Argentina · Trabajo remoto"; H1 exacto "El problema ya lo tenés. Falta el documento que lo resuelve."; lead exacto "Analizo el problema, comparo alternativas con datos y normativa, y te entrego un documento técnico listo para que un profesional lo valide y tu equipo lo ejecute. Sin prototipos. Sin dirección de obra."; CTA "Contame tu problema" a `contacto.html`; CTA texto "Ver un documento real →" a `documento.html`.

- [ ] **Step 3: Escribir la hoja A4 del hero**

`figure.sheet` con cabecera "IRD · Documento de solución" / "SOL-001", título "Optimización de procesos", subtítulo "Resumen ejecutivo · Rev. A", párrafo, etiqueta "03 · Alternativas evaluadas", tabla de 3 alternativas (A/B/C) con costo/plazo/riesgo, etiqueta "05 · Resultado esperado", párrafo y sello "Muestra". La tabla debe ser legible en desktop y reducirse en móvil.

- [ ] **Step 4: Escribir la ficha del servicio**

`div.spec` con encabezado "Ficha del servicio" / "Rev. 01" y 8 filas: Entregable PDF + fuente LaTeX; Estructura 8 secciones fijas; Alternativas mínimo 3, comparadas; Plazo 15 a 25 días; Alcance diseño y documentación; No incluye ejecución y firma; Inversión desde USD 1.200; Modalidad remota, todo el país y el exterior.

- [ ] **Step 5: Escribir "No vendo horas" y "IRD documenta. No ejecuta."**

Sección 02 con 4 pasos: 01 Problema y causa raíz; 02 Alternativas comparadas; 03 Solución recomendada; 04 Resultado y límites. Link a `documento.html`. Sección 03 con dos columnas "Lo que hago" / "Lo que no hago" y el bloque de honestidad: "IRD no firma proyectos ni reemplaza a un ingeniero matriculado. Entrega documentación técnica para que un profesional habilitado la valide y la firme cuando corresponda."

- [ ] **Step 6: Escribir la preview del documento**

Tres imágenes (`muestra-p1.jpg`, `muestra-p2.jpg`, `muestra-p3.jpg`) con alt descriptivo, botón "Descargar muestra en PDF" a `assets/docs/muestra-SOL-001.pdf`, y nota "Muestra de formato. Contenido ilustrativo. No es un caso real. La muestra está abreviada; un documento real suele tener 18–25 páginas."

- [ ] **Step 7: Escribir método, laboratorio, sobre mí, precios, FAQ y CTA**

Método 4 pasos (consulta USD 80; alcance y presupuesto 7 días; investigación 15–25 días; entrega y 2 rondas). Laboratorio con biomasa 45%, "Revisión octubre 2026", "No es un caso de éxito. Es un proyecto abierto." Sobre mí con UTN Reconquista y 3º año en curso. Precios: 3 tarjetas + complejo desde USD 3.000 + acompañamiento USD 300 + nota de moneda/inflación. FAQ de 6 preguntas. CTA final con email y link a contacto.

- [ ] **Step 8: Verificar**

Run: `powershell -ExecutionPolicy Bypass -File tools/check_site.ps1`
Expected: solo fallan las páginas que todavía no existen y las imágenes OG.

Abrir `index.html` con `browser.preview` y sacar screenshots a 1440px y 390px. Confirmar: sin overflow, H1 legible, hoja A4 no tapa la ficha, CTA visible.

---

### Task 5: El documento en español

**Files:**
- Create: `documento.html`

**Interfaces:**
- Consumes: `assets/img/muestra-p1.jpg` … `p3`, `assets/docs/muestra-SOL-001.pdf`.
- Produces: enlaces a `contacto.html` y `terminos.html`.

- [ ] **Step 1: Escribir `<head>`, header y page hero**

Title `El documento de solución · IRD`; description sobre las 8 secciones, alternativas y entrega en PDF + LaTeX. H1 "El documento de solución". Lead "Qué recibís, cómo se ve y cuánto cuesta." CTA "Descargar muestra" y "Pedir presupuesto".

- [ ] **Step 2: Escribir la banda de datos**

4 celdas: `03+` Alternativas por caso; `08` Secciones fijas; `100%` Supuestos declarados; `00` Prototipos físicos.

- [ ] **Step 3: Escribir la anatomía de 8 secciones**

01 Resumen ejecutivo; 02 Problema detectado; 03 Alternativas evaluadas; 04 Solución recomendada; 05 Resultado esperado; 06 Qué NO incluye; 07 Condiciones de uso y licencia; 08 Anexos. Cada una con una frase de qué responde.

- [ ] **Step 4: Escribir la muestra y los límites**

3 imágenes + botón de descarga + nota de muestra abreviada. Dos columnas "Incluye" / "No incluye" con las listas del diseño. Callout "Cómo se valida": el documento le ahorra al profesional reconstruir el problema; su trabajo es revisar, ajustar y firmar.

- [ ] **Step 5: Escribir proceso, precios y qué necesito**

Timeline de 6 pasos. Tabla de precios con Producto / Precio / Horas / Plazo / Para quién (consulta, diagnóstico, completo, complejo, acompañamiento). Nota de moneda, MEP +5%, 7 días, IPC, 50/50. Lista "Qué necesito de vos": datos, acceso, responsable, 2–3 h de entrevistas, decisiones de restricción.

- [ ] **Step 6: Escribir FAQ y CTA**

5 preguntas: cambios (2 rondas), cambio de alcance, propiedad/licencia, publicación, falta de datos. CTA a contacto.

- [ ] **Step 7: Verificar**

Checker + preview desktop/mobile. Confirmar que las imágenes cargan, la tabla no desborda y los links a la muestra funcionan.

---

### Task 6: Laboratorio, Sobre mí y Contacto en español

**Files:**
- Create: `laboratorio.html`, `sobre-mi.html`, `contacto.html`

**Interfaces:**
- Consumes: CSS/JS compartidos, email.
- Produces: formulario `#contact-form` con campos `nombre`, `email`, `pais`, `empresa`, `problema`, `probaste`, `plazo`, `presupuesto`, `origen`, `consentimiento`, `website` (honeypot).

- [ ] **Step 1: Escribir `laboratorio.html`**

Hero "El laboratorio" + "Investigación propia, sin cliente. Acá está lo que estoy aprendiendo y lo que todavía no sé." Proyecto 001: biomasa, estado 45%, revisión octubre 2026, problema, hipótesis, qué está resuelto, qué falta, próximo hito sin fecha inventada, aviso "No es un caso de éxito ni un producto terminado." CTA a contacto. Sección "Cómo se convierte en proyecto" con 3 pasos. Sin bitácora inventada.

- [ ] **Step 2: Escribir `sobre-mi.html`**

Hero con nombre y rol. Ficha con formación (3º año Ingeniería Electromecánica, UTN Facultad Regional Reconquista, en curso), foco, idiomas, modalidad. Monograma "SB" (sin foto). Secciones: por qué existe IRD; 4 principios; lo que sí/no; validación profesional. CTA.

- [ ] **Step 3: Escribir `contacto.html`**

Hero "Contame tu problema." + "No necesito un brief perfecto. Con estas preguntas alcanza para saber si puedo ayudarte." Formulario con los campos de la interfaz, labels visibles, `required` en nombre/email/problema/consentimiento, honeypot oculto, botón "Preparar el mensaje". Debajo: email visible, "Respondo en 24–48 h hábiles", "Qué pasa después" (3 pasos), nota de alcance y nota de pago internacional.

- [ ] **Step 4: Verificar**

Checker + preview. Probar el formulario con datos de ejemplo y confirmar que se abre el `mailto:` con el cuerpo completo. Probar sin JavaScript: el formulario debe tener `action="mailto:sebabergesio472@gmail.com"` y el email visible.

---

### Task 7: Términos y 404

**Files:**
- Create: `terminos.html`, `404.html`

- [ ] **Step 1: Escribir `terminos.html`**

14 secciones: identificación; objeto y alcance; presupuesto y precios; pago y actualización; plazos; revisiones; responsabilidades del cliente; propiedad intelectual; confidencialidad; límite de responsabilidad; cancelación; privacidad (Ley 25.326); ley aplicable y jurisdicción; contacto. Fecha "octubre 2026". Sin afirmar revisión legal. Incluir la frase de que no firma proyectos ni reemplaza a un matriculado.

- [ ] **Step 2: Escribir `404.html`**

Bilingüe, en dos columnas: "404 · Página no encontrada" / "Page not found"; mensaje y links a Home, El documento, Contacto / Home, The document, Contact. Mismo header simplificado y footer. Sin `canonical` (o canonical a la home) y con `noindex`.

- [ ] **Step 3: Verificar**

Checker (el 404 puede exceptuar hreflang) + preview.

---

### Task 8: Páginas en inglés

**Files:**
- Create: `en/index.html`, `en/document.html`, `en/lab.html`, `en/about.html`, `en/contact.html`, `en/terms.html`

**Interfaces:**
- Consumes: `../assets/...`, `../index.html`, `../documento.html`, `../laboratorio.html`, `../sobre-mi.html`, `../contacto.html`, `../terminos.html`.
- Produces: pares bilingües completos.

- [ ] **Step 1: Traducir la home**

Title `IRD · Technical documentation for engineering problems`. H1 "You already have the problem. What's missing is the document that solves it." Lead: "I analyze the problem, compare alternatives against data and applicable standards, and deliver a technical document ready for a qualified professional to validate and your team to execute. No prototypes. No construction management." Nav: The document / Lab / About / Contact. CTA "Tell me what's not working". Mantener la misma estructura, ficha, hoja, pasos, precios y FAQ.

- [ ] **Step 2: Traducir El documento**

Title `The solution document · IRD`. Misma anatomía, banda, muestra EN (`muestra-en-p1.jpg`…), límites, proceso, tabla de precios, FAQ y CTA.

- [ ] **Step 3: Traducir Laboratorio, Sobre mí y Contacto**

Lab: "Independent research, no client. This is what I'm learning and what I don't know yet." About: same bio and limits. Contact: form fields in English; email; "I reply within 24–48 business hours." Form action same email; subject "Website inquiry".

- [ ] **Step 4: Traducir Términos y privacidad**

Same 14 sections in English. Jurisdiction Argentina, Santa Fe. No legal-review claim.

- [ ] **Step 5: Verificar paridad**

Checker. Confirmar que cada ES tiene EN y viceversa, que los links `../` resuelven y que el selector de idioma lleva a la página equivalente (no a la home).

---

### Task 9: Assets SEO, sitemap y robots

**Files:**
- Create: `tools/og-es.html`, `tools/og-en.html`
- Create: `assets/img/og-ird-es.png`, `assets/img/og-ird-en.png`
- Create: `robots.txt`, `sitemap.xml`
- Modify: all pages (JSON-LD, OG image paths)

- [ ] **Step 1: Crear las tarjetas OG**

`tools/og-es.html` y `tools/og-en.html`: body de 1200×630, fondo papel con grilla, logo, eyebrow "IRD · Documento técnico", titular y pie "Reconquista, Argentina · Trabajo remoto". Sin precios. Abrir con `browser.preview`, sacar screenshot fullPage y guardar como PNG en `assets/img/`.

- [ ] **Step 2: Verificar dimensiones**

```powershell
Add-Type -AssemblyName System.Drawing
$img = [System.Drawing.Image]::FromFile((Resolve-Path assets/img/og-ird-es.png))
"$($img.Width)x$($img.Height)"
```

Expected: `1200x630`. Repetir para EN.

- [ ] **Step 3: Escribir `robots.txt`**

```
User-agent: *
Allow: /
Disallow: /_legacy/
Sitemap: https://ird.example/sitemap.xml
```

- [ ] **Step 4: Escribir `sitemap.xml`**

12 URLs (6 ES + 6 EN), `lastmod` 2026-10-21, sin el 404. Incluir `xhtml:link` alternates para cada par.

- [ ] **Step 5: Agregar JSON-LD**

En la home ES y EN: `ProfessionalService` con nombre, url, email, founder, areaServed, priceRange, address. En `documento.html` y `en/document.html`: `Service` con name, description, provider, areaServed, offers (priceCurrency USD, priceSpecification min 450). En las páginas con FAQ visible: `FAQPage` con las preguntas exactas. Sin `aggregateRating` ni `Review`.

- [ ] **Step 6: Verificar**

Checker + validar JSON-LD con `ConvertFrom-Json` y confirmar que las OG existen y miden 1200×630.

---

### Task 10: QA final, README y publicación

**Files:**
- Create: `README.md`, `tools/publish.ps1`
- Create: `dist/` (generado)

- [ ] **Step 1: Ejecutar el checker completo**

Run: `powershell -ExecutionPolicy Bypass -File tools/check_site.ps1`
Expected: PASS, 0 errores.

- [ ] **Step 2: Revisar responsive**

Abrir `index.html`, `documento.html`, `laboratorio.html`, `sobre-mi.html`, `contacto.html`, `terminos.html` y sus pares EN a 1440px y 390px. Confirmar: sin scroll horizontal, menú funcional, ficha legible, tablas con scroll interno, footer ordenado.

- [ ] **Step 3: Revisar accesibilidad**

Navegar con Tab: skip link, nav, menú, FAQ, formulario, footer. Confirmar foco visible, labels, `aria-current`, contraste y `prefers-reduced-motion`.

- [ ] **Step 4: Revisar contenido**

Buscar `ird.com.ar`, `45.000`, `catálogo`, `asistente`, `consultora`, `constructora`, `garantizado`, `lorem`, `TBD`, `TODO`. Confirmar que no queden en el sitio público. Confirmar que la frase de no firma aparece en home, documento, sobre mí y términos.

- [ ] **Step 5: Escribir `README.md`**

Qué es el sitio; cómo previsualizar (`start index.html` o servidor local); dónde están diseño y plan; cómo publicar (`tools/publish.ps1` y subir `dist/`); pendientes (dominio, correo, cobro, foto, endpoint del formulario); cómo editar precios y textos.

- [ ] **Step 6: Escribir `tools/publish.ps1`**

Copiar a `dist/`: los 7 HTML de la raíz, `en/`, `assets/`, `robots.txt`, `sitemap.xml`. Excluir `_legacy`, `documentos`, `Recursos`, `herramientas`, `docs`, `tools`, `*.tex`, `*.log`, `*.aux`. Verificar que `dist/index.html` exista y que `dist/_legacy` no exista.

- [ ] **Step 7: Generar `dist/` y verificar**

```powershell
powershell -ExecutionPolicy Bypass -File tools/publish.ps1
Get-ChildItem dist -Recurse -File | Measure-Object
```

Expected: `dist/index.html`, `dist/en/index.html`, `dist/assets/css/style.css`, `dist/robots.txt`, `dist/sitemap.xml`; sin `_legacy`.

- [ ] **Step 8: Presentar al usuario**

Abrir `dist/index.html` con `browser.preview`, sacar screenshots desktop/mobile y mostrar el resultado. Informar pendientes: dominio, correo profesional, cobro internacional, foto y endpoint del formulario.

---

## Self-Review

**1. Cobertura del spec:** cada sección del diseño tiene tarea: arquitectura (Tasks 1, 8), home (4), documento (5), laboratorio/sobre mí/contacto (6), términos/404 (7), precios (4, 5), muestras (2), SEO (9), publicación (10), accesibilidad (3, 10), contenido legal (7).

**2. Pasos:** cada paso produce un archivo o una verificación concreta; no hay "TBD" ni "manejar casos" sin archivo.

**3. Consistencia:** clases y nombres de campos coinciden entre CSS, JS y HTML; las rutas ES/EN están definidas; los precios son los mismos en todas las páginas.

**4. Review Focus:** los cinco riesgos tienen verificación en Task 1 (checker), Task 8 (paridad/links), Task 10 (contenido, responsive, formulario).

**5. Proporción:** el plan describe decisiones y verificaciones; el código se escribe en la ejecución, no se transcribe acá.
