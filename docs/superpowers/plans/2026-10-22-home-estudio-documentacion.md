# Home como página de estudio de documentación técnica

## Goal

Reestructurar el home público de IRD para que se lea como la página de un
estudio de documentación técnica —no como la página de un producto—, con el
orden y el copy que fijó el cliente, tipografía y contraste legibles en todo el
sitio, navegación simple de seis ítems y publicación en GitHub Pages. Los
precios y plazos reales se conservan; no se inventan datos, clientes ni
métricas.

## Architecture

Sitio estático generado: `tools/build_site.py` combina `src/layout.html` con
los fragmentos de `src/pages/*.html` y escribe `site/*.html` +
`sitemap.xml`. Los assets (CSS, JS, imágenes, PDF) viven directamente en
`site/assets/` y se editan ahí. `tools/check_site.py` valida metadata,
enlaces, paridad ES/EN, cadenas prohibidas y —a partir de este plan— estructura
del home, navegación y tipografía del CSS. `site/assets/js/rates.js` llena los
precios en ARS desde `data-usd`/`data-price-ars`, sin cambios.

La publicación usa `tools/publish_pages.ps1` (build + check + `git subtree
push --prefix site site master` al repo público `sebabergesio/ird-site`).

## Tech Stack

- Python 3 (stdlib) para build, checks y suite de tests.
- HTML/CSS/JS estático sin frameworks.
- PowerShell para el script de publicación.
- Git con subtree hacia el repo público de Pages.

## Spec

Brief del cliente (2026-10-22), transcripto en «Global Constraints». Los
precios y plazos vigentes en el sitio son la fuente de verdad y no cambian:
Consulta USD 80 (1 h, se descuenta), Diagnóstico express USD 450–500
(7–10 días, 8–12 páginas), Documento completo desde USD 1.200 (15–25 días,
18–25 páginas), Proyecto complejo desde USD 3.000, Acompañamiento USD 300/mes.

## Global Constraints

- Orden del home: 1 hero sin precios · 2 qué es IRD y quién lo hace ·
  3 problema que resuelve · 4 método · 5 ejemplo de documento · 6 qué recibe ·
  7 planes/plazos/precios · 8 límites (una sola vez, al final) · 9 FAQ ·
  10 contacto.
- Hero exacto (ES): título «IRD — Documentación técnica para decisiones
  industriales»; subtítulo «Estudio de documentación técnica. Desarrollamos tu
  idea o problema, presentamos otras soluciones posibles y concluimos si es
  técnicamente viable, con supuestos y límites.»; bajada «Sin estimación de
  costos, sin ejecución y sin firma: el documento es para que tu equipo decida
  y ejecute.»; botones «Ver un ejemplo de documento» y «Consultar mi caso».
- Límites exactos (ES): «IRD no firma como ingeniero matriculado, no ejecuta
  obras, no dirige obra, no fabrica equipos, no hace prototipos físicos para
  clientes y no garantiza resultados de terceros. La validación y firma
  profesional las realiza un matriculado del cliente o un tercero habilitado.»
  «no firma» y «no ejecuta» deben aparecer exactamente 1 vez en el home
  (EN: «does not sign» / «does not execute», 1 vez).
- Qué recibe: problema y causa raíz, otras soluciones posibles, solución
  desarrollada, cálculos y supuestos, límites, conclusión de viabilidad
  técnica, próximos pasos. Nota exacta: «Sin estimación de costos, sin análisis
  de rentabilidad, sin comparación económica y sin plan de ejecución, salvo que
  el cliente lo solicite aparte.»
- Precios como «niveles de alcance según urgencia y complejidad»; cada plan
  dice qué incluye y qué no; aclarar que el plazo depende de complejidad y
  urgencia. Ningún precio de servicio antes de la sección 7.
- Tipografía: nada <14px; cuerpo ≥16px (17–18 ideal); line-height ≥1.6;
  precios/datos destacados ≥20px; H1 clamp(32px, 5vw, 56px); H2
  clamp(26px, 3.5vw, 40px); H3 ≥20px; contraste AA (#1A1A1A primario,
  secundario no más claro que #4A4A4A); líneas de 70–75 caracteres; mobile:
  cuerpo ≥16px, botones de 44px de alto y texto ≥16px; nada de párrafos en
  mayúsculas sostenidas.
- Nav: Inicio / Qué es IRD / Método / Ejemplo / Alcance y precios / Contacto
  (EN: Home / About IRD / Method / Example / Scope & pricing / Contact).
- Sin testimonios, logos, clientes, casos, años ni métricas inventadas.
- Paridad ES/EN verificada por `check_site.py`; sin cadenas prohibidas
  («LaTeX», «PDF +», «Reconquista, Santa Fe», «10–15 días»).

## Decisiones (rulings)

1. Bajada del hero: «Sin costos» se reemplaza por «Sin estimación de costos»
   para que no se lea como servicio gratuito (alineado con «no incluye costos»
   y con el criterio 6 del cliente).
2. Se quita el botón CTA del header y del menú móvil; «Contacto» en la nav
   cubre la conversión.
3. La hoja A4 del hero se conserva tal cual (es la muestra del entregable; sus
   importes ilustrativos no cuentan como precio de servicio en los chequeos).
4. Precios en orden ascendente de alcance: Consulta (nivel 1), Diagnóstico
   (nivel 2), Documento completo (nivel 3, destacado).
5. FAQ reducida a 5 preguntas; se quitan las de firma/prototipos para no
   repetir los límites y se agrega «¿Incluye costos, rentabilidad o plan de
   ejecución?».
6. Se ejecuta inline sobre `master` (repo de un solo autor; flujo establecido
   de commits + subtree push).

## Review Focus

1. Mobile 320–640 px: la nav de 6 ítems no desborda, botones ≥44 px, la hoja
   del hero y las tablas no generan scroll horizontal con el texto a 14 px.
2. ARS en vivo: `rates.js` sigue llenando los 5 importes (`data-usd` intactos)
   después de reordenar las tarjetas; si falla, las conversiones quedan vacías.
3. Anclas entre páginas: «Alcance y precios» desde `documento.html` y demás
   páginas resuelve a `index.html#precios` y aterriza bajo el header fijo.
4. Paridad EN: cada cambio ES tiene espejo EN; los conteos de límites en EN
   también dan 1 y los hreflang siguen apuntándose entre sí.
5. Contraste de textos secundarios sobre fondo oscuro (tarjeta featured, CTA,
   footer): el gris de nota debe seguir ≥4.5:1 sobre tinta.

---

## Tarea 1 — Estructura y copy del home ES/EN + chequeos estructurales

**Files:** `tools/check_site.py`, `src/pages/home.es.html`,
`src/pages/home.en.html`, `tools/build_site.py` (metas del home).

**Interfaces:**

- `HOME_STRUCTURE: dict[str, dict]` con, por ruta pública:
  `sections` (ids en orden), `pricing_id`, `once` (frases que deben aparecer
  una sola vez).
  - `index.html`: `["que-es-ird", "problema", "metodo", "ejemplo",
    "que-recibe", "precios", "limites", "preguntas"]`, pricing `precios`,
    once `["no firma", "no ejecuta"]`.
  - `en/index.html`: `["about-ird", "problem", "method", "example",
    "what-you-get", "pricing", "limits", "faq"]`, pricing `pricing`,
    once `["does not sign", "does not execute"]`.
- `SERVICE_PRICE_MARKERS` = `["data-usd=", "data-price-ars", "USD 80",
  "USD 450", "USD 1.200", "USD 1.400", "USD 3.000", "USD 300", "Desde USD",
  "desde USD", "From USD", "from USD"]` (excluye a propósito los importes
  ilustrativos de la hoja: USD 6.000/10.000).
- `check_home_structure(root: Path) -> list[str]`: verifica existencia de ids,
  orden estricto, ausencia de marcadores de precio de servicio entre `<main` y
  el id de precios, y conteo exacto = 1 de cada frase de `once`.

**Steps:**

- [ ] Agregar `HOME_STRUCTURE`, `SERVICE_PRICE_MARKERS`,
      `check_home_structure()` y llamarla desde `main()`.
- [ ] `python tools/check_site.py` → RED (secciones faltantes/desordenadas,
      precios antes de `#precios`, conteos ≠ 1). Registrar evidencia.
- [ ] Reescribir `home.es.html` con este orden y copy:
      - Hero: strings exactos del brief (bajada con «Sin estimación de
        costos»), botones en el orden pedido («Ver un ejemplo de documento» →
        `#ejemplo`, «Consultar mi caso» → `contacto.html`), nota de respuesta
        24–48 h. Hoja A4 intacta.
      - 01 `#que-es-ird` «Un estudio de documentación técnica»: qué es, quién
        lo hace (Sebastián Bergesio, fundador; estudiante avanzado de
        Electromecánica, UTN Reconquista; un solo responsable), para quién sí
        y para quién no (PyME, emprendedores, estudios de ingeniería; no horas
        sueltas de CAD ni quien no aporta datos), ficha de 4 datos y enlace a
        `sobre-mi.html`.
      - 02 `#problema` «Saber si es posible, antes de invertir, licitar o
        ejecutar»: problema/idea; conclusión de viabilidad técnica con
        supuestos y límites; el cliente decide, aprueba y ejecuta.
      - 03 `#metodo`: lista vertical `.method` de 7 pasos (relevamiento,
        análisis técnico, otras soluciones posibles, conclusión de viabilidad,
        entrega, revisión y aprobación del cliente, ejecución por el cliente) +
        nota «nivel de desarrollo técnico a medida».
      - 04 `#ejemplo`: bloque `doc-preview` actual con `id="ejemplo"` y
        numeración 04.
      - 05 `#que-recibe`: lista de 7 entregables + nota exacta en `.honesty`.
      - 06 `#precios`: «Tres niveles, según urgencia y complejidad»; tarjetas
        ascendentes Consulta → Diagnóstico → Documento completo (featured);
        cada una con incluye/no incluye (`.price-excl`); notas de plazo,
        moneda y validez actuales. Conservar `pricing-extra`.
      - 07 `#limites`: bloque `.limits` con el texto exacto.
      - 08 `#preguntas`: 5 FAQ (qué necesitás, cuánto tarda, cómo se paga,
        exterior, incluye costos/rentabilidad/plan).
      - 09 CTA de contacto actual, renumerado.
      - JSON-LD con la nueva descripción.
- [ ] Espejo EN con los ids y strings equivalentes.
- [ ] Actualizar title/description del home (ES/EN) en `PAGES` de
      `tools/build_site.py` (sin precios; encuadre de estudio).
- [ ] `python tools/build_site.py` + `python tools/check_site.py` → GREEN.
- [ ] Commit: `feat(home): reestructurar el home como página del estudio`.

## Tarea 2 — Navegación simple y header/footer

**Files:** `tools/build_site.py`, `tools/check_site.py`, `site/*.html`
(generados).

**Interfaces:**

- `NAV: dict[str, list[tuple[str, str, str]]]` → `(page_key, label, anchor)`:
  ES Inicio/`""`, Qué es IRD/`que-es-ird`, Método/`metodo`, Ejemplo/`ejemplo`,
  Alcance y precios/`precios`, Contacto/`""` (`contacto`); EN Home/`""`,
  About IRD/`about-ird`, Method/`method`, Example/`example`, Scope &
  pricing/`pricing`, Contact/`""` (`contacto`).
- `nav_href(page, key, anchor) -> str`: `href(page, PATHS[lang][key])` +
  `#anchor` si corresponde.
- `NAV_EXPECTED` en `check_site.py` + `check_nav(root)`: las etiquetas del
  primer `<nav class="nav-desktop">` de `index.html` y `en/index.html` deben
  ser exactamente las seis esperadas, en orden.
- Header y menú móvil sin CTA; `footer_tagline` pasa a encuadre de estudio.

**Steps:**

- [ ] Agregar `NAV_EXPECTED` + `check_nav()` y llamarla desde `main()`.
- [ ] `python tools/check_site.py` → RED (etiquetas viejas).
- [ ] Cambiar `NAV`, agregar `nav_href()`, usarlo en header y footer; quitar
      los dos CTA y las claves `cta` de `COPY`; actualizar `footer_tagline`
      ES/EN; ajustar el ítem activo.
- [ ] `python tools/build_site.py` + `python tools/check_site.py` → GREEN.
- [ ] Commit: `feat(nav): navegación simple de seis ítems y header sin CTA`.

## Tarea 3 — Tipografía, contraste y legibilidad en todo el sitio

**Files:** `site/assets/css/style.css`, `tools/check_site.py`.

**Interfaces:**

- `check_css_typography(root: Path) -> list[str]`: para cada `font-size` del
  CSS, todos los valores en px deben ser ≥14 y no se admiten `em`/`rem`; el
  bloque `body {}` debe declarar `line-height` ≥1.6.

**Steps:**

- [ ] Agregar `check_css_typography()` y llamarla desde `main()`.
- [ ] `python tools/check_site.py` → RED con la lista de declaraciones
      <14 px y el line-height del body.
- [ ] Tokens y base: `--ink:#1A1A1A`, `--muted:#4A4A4A`, líneas
      `rgba(26,26,26,…)` (incluidos los gradientes del fondo), cuerpo
      17 px/1.65.
- [ ] Escala: `.mono` y textos secundarios ≥14; nav 15; `.btn` 15 con
      `min-height:44px` (móvil 16/48); `.btn-text` 16; `.lead` 18; H1
      clamp(32px,5vw,56px); H2 clamp(26px,3.5vw,40px); H3 ≥20; precios/datos
      destacados ≥20 (`.price .price-ars` 20); tabla, ficha, hoja A4, footer,
      legales y formularios ≥14/16 según corresponda.
- [ ] Ancho de línea: override final para prosa (`main p`, `main li`, `.faq p`,
      `.honesty`, `.doc-note`, `.rate-note`, `.legal-body`, `.about-teaser p`)
      a `max-width:72ch`.
- [ ] Estilos nuevos: `.method` (lista vertical numerada), `.limits`
      (bloque sobrio, sin color de advertencia), `.price-excl`, `.hero-bajada`.
      Eliminar las reglas `.band` y `.spec*` (solo las usaba el home). Ajustar
      `.timeline` (lo usa `documento`).
- [ ] Móvil: quitar los overrides de H1 y de `.section-head h2`; `.lead` 17;
      `.menu-nav a` 16 con 44 px de alto; `.lang-switch` usable; botones ≥44.
- [ ] `python tools/build_site.py` + `python tools/check_site.py` → GREEN.
- [ ] Smoke visual con navegador (home, documento, contacto a 360 px y
      1280 px). Commit: `fix(css): tipografía y contraste legibles en todo el sitio`.

## Tarea 4 — Build completo, suite y auditoría de criterios

**Steps:**

- [ ] `python tools/build_site.py` (todas las páginas + sitemap).
- [ ] `python tools/check_site.py` → 0 errores.
- [ ] `python -m unittest discover -s tools/tests -v` → todo verde.
- [ ] Verificar a mano los 10 criterios del cliente y registrar evidencia en el
      ledger (hero en 5 s, sin precios antes de 7, límites una sola vez,
      cliente decide/ejecuta, sin textos <14 px).
- [ ] Commit de lo que reste (generados/sitemap).

## Tarea 5 — Publicar y verificar en vivo

**Steps:**

- [ ] `git push origin master`.
- [ ] `powershell -ExecutionPolicy Bypass -File tools/publish_pages.ps1`.
- [ ] Descargar `https://sebabergesio.github.io/ird-site/` y `en/index.html`;
      verificar hero nuevo, nav de 6, límites 1 vez y ausencia de precios antes
      de `#precios`.
- [ ] Confirmar estado de Pages (`gh api repos/sebabergesio/ird-site/pages`).
- [ ] Revisión final con subagente (`general`, template de code review) y un
      solo pase de fixes; reportar rulings al cliente.
