# IRD Website Rebuild — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the old IRD site with a bilingual, static, document-first site that sells one full technical document per month.

**Architecture:** Plain HTML output, one shared CSS file, one small JS file. A local Python generator assembles the 13 pages from a single layout plus per-page HTML fragments, so nav, footer, hreflang and metadata stay consistent. The published site is plain static HTML and does not need the generator at runtime. A Python checker verifies metadata, links, language parity and banned strings.

**Tech Stack:** HTML5, CSS (custom properties, grid), vanilla JS, Python 3.13 stdlib, MiKTeX (`pdflatex`), Poppler (`pdftoppm`), PowerShell for publish. Git for snapshots.

**Spec:** `docs/superpowers/specs/2026-10-21-ird-website-design.md`

## Global Constraints

- Spanish at root; English under `/en/`. `lang="es"` / `lang="en"`. hreflang `es-AR`, `en`, `x-default` (Spanish).
- Prices: consultation USD 80; express diagnosis USD 450–500 (7–10 days); full document USD 1.200–1.400 (15–25 days); complex from USD 3.000; monthly support USD 300.
- Payment copy: USD reference; ARS at MEP + 5%; quote valid 7 days; unpaid balances adjusted by IPC; 50% upfront / 50% on delivery.
- Never claim IRD signs, executes, prototypes or replaces a licensed engineer. The validation-by-a-licensed-professional line must appear on home, document, about and terms.
- No invented cases, testimonials, metrics, dates or portfolio. Biomass is “research in progress, 45%, reviewed October 2026”.
- `ird.com.ar` is forbidden: it belongs to another company. Use `https://ird.example` as the site URL placeholder and remove the domain from the sample PDF cover.
- No frameworks, no npm, no runtime build. Google Fonts only external dependency.
- Visual system: paper `#F1F0EA`, ink `#111417`, teal `#0B6B6B`, accent `#C2410C`, accent-bright `#D9480F`, mono labels, sharp corners.
- Accessibility: AA contrast, visible focus, skip link, keyboard nav, `prefers-reduced-motion`, labels on all form fields.
- All public HTML must pass `herramientas/check_site.py` and open from `file://` with relative links.

## Review Focus

1. **Price/time consistency:** a visitor must never see “desde USD 450” next to “8 secciones / 15–25 días”. The full document is the hero product; the diagnosis is an entry product.
2. **Bilingual path correctness:** `/en/` pages must resolve `../assets/`, `../index.html`, `document.html` and `../documento.html` correctly from `file://` and from a static host.
3. **Honesty about the licensed engineer:** the student/matriculation limitation must survive translation and not be buried in terms.
4. **Sample PDF integrity:** the downloadable sample must not show `ird.com.ar`, must be labeled as illustrative, and must not look like a real client case.
5. **Mobile navigation and long tables:** the spec table, pricing table and document preview must not overflow at 320–390px.

---

## File Structure

```
IRD/
  index.html, documento.html, laboratorio.html, sobre-mi.html,
  contacto.html, terminos.html, 404.html          (generated, public)
  en/index.html, en/document.html, en/lab.html,
  en/about.html, en/contact.html, en/terms.html    (generated, public)
  assets/
    css/style.css
    js/site.js
    img/logo-negro.svg, logo-blanco.svg, favicon.svg,
        og-ird-es.png, og-ird-en.png,
        muestra-p1.jpg, muestra-p2.jpg, muestra-p3.jpg,
        muestra-en-p1.jpg, muestra-en-p2.jpg, muestra-en-p3.jpg
    docs/muestra-SOL-001.pdf, muestra-SOL-001-en.pdf
  robots.txt, sitemap.xml                          (generated)
  src/
    layout.html
    pages/*.html                                   (content fragments)
    og/og-es.html, og-en.html
  herramientas/
    build_site.py
    check_site.py
    publish.ps1
    build_samples.ps1
  _legacy/                                         (old files, not published)
  docs/                                            (spec + plan, not published)
  documentos/, Recursos/                           (sources, not published)
```

**Interfaces**

- `build_site.py`:
  - `SITE_URL = "https://ird.example"`
  - `PAGES: list[dict]` with `key`, `lang`, `out`, `title`, `description`, `nav`, `og_image`, `body_class`
  - `render(lang, active, title, description, canonical, alt_es, alt_en, og_image, body_class, content) -> str`
  - `write_pages()`, `write_sitemap()`
  - CLI: `python herramientas/build_site.py`
- `check_site.py`:
  - `check_page(path, root) -> list[str]`
  - `check_links(root) -> list[str]`
  - `check_parity() -> list[str]`
  - `check_banned(root) -> list[str]`
  - CLI: `python herramientas/check_site.py [--root .]`; exit 1 on errors.
- `site.js`:
  - closes mobile `<details>` on link click
  - `IntersectionObserver` reveal, respects reduced motion
  - sets current year
  - contact form: validates required fields, builds `mailto:` with encoded subject/body
- `build_samples.ps1`:
  - copies `documentos/ejemplo-SOL-001.tex` and `Recursos/LogoNegro.png` to a temp build dir
  - removes `ird.com.ar` from the cover
  - compiles twice with `pdflatex`
  - renders pages 1, 3, 4 to JPEG at 120 dpi, quality 82
  - copies PDFs to `assets/docs/`, JPEGs to `assets/img/`
  - repeats for the English translation (`src/docs/muestra-SOL-001-en.tex`)

---

### Task 0: Safety net and baseline

**Files:**
- Create: `.gitignore`
- Create: `_legacy/README.md`

- [ ] **Step 1: Initialize git and commit the current site**

```powershell
$git = 'C:\Program Files\Git\cmd\git.exe'
& $git init
& $git config user.name "Sebastian Bergesio"
& $git config user.email "sebabergesio472@gmail.com"
```

Add `.gitignore`:

```
_legacy/
dist/
__pycache__/
*.aux
*.log
*.out
*.toc
src/docs/build/
```

- [ ] **Step 2: Commit baseline**

```powershell
& $git add .
& $git commit -m "chore: baseline before IRD redesign"
```

Expected: commit created; `git status` clean except ignored dirs.

---

### Task 1: Test harness, layout, tokens, JS

**Files:**
- Create: `herramientas/check_site.py`
- Create: `herramientas/build_site.py`
- Create: `src/layout.html`
- Create: `assets/css/style.css`
- Create: `assets/js/site.js`
- Create: `assets/img/logo-negro.svg`, `assets/img/logo-blanco.svg`

- [ ] **Step 1: Write the failing checker**

`check_site.py` must:
- parse each HTML file in root and `en/`
- require `<title>`, `meta[name=description]`, `link[rel=canonical]`, `link[hreflang=es-AR]`, `link[hreflang=en]`, `link[hreflang=x-default]`
- require `lang="es"` on root pages and `lang="en"` on `/en/` pages
- check every `href`/`src` that is not `http`, `https`, `mailto:`, `tel:`, `#` resolves to an existing file
- check language parity: every ES page has the matching EN page and vice versa
- fail on `ird.com.ar`, `data.js`, `soluciones.html`, `producto.html`, `asistente.html`, `admin.html`
- fail on `TODO` or `ird.example` in public HTML except canonical/hreflang/OG URLs
- exit 1 with a list of errors

Run against the old `index.html`:

```powershell
G:\Python313\python.exe herramientas\check_site.py --root .
```

Expected: FAIL (no canonical/hreflang, old links).

- [ ] **Step 2: Build the generator and a minimal home**

Create `src/layout.html` with placeholders `{{LANG}}`, `{{TITLE}}`, `{{DESCRIPTION}}`, `{{CANONICAL}}`, `{{ALT_ES}}`, `{{ALT_EN}}`, `{{OG_IMAGE}}`, `{{BODY_CLASS}}`, `{{HEADER}}`, `{{CONTENT}}`, `{{FOOTER}}`, `{{ASSET_PREFIX}}`.

Create `build_site.py` that:
- reads `src/layout.html`
- builds header/footer from page list and language
- computes relative paths: ES `link_es(p)=p`, `link_en(p)="en/"+p`; EN `link_es(p)="../"+p`, `link_en(p)=p`; assets `""` vs `"../"`
- writes `index.html` for the first page
- writes `sitemap.xml` with all pages

- [ ] **Step 3: Create CSS tokens and base**

`style.css` must define the tokens from the spec, reset, typography, `.wrap`, header/nav, buttons, section, footer, responsive breakpoints at 900/640px. No rounded corners except the stamp and favicon.

- [ ] **Step 4: Create JS**

`site.js` as described in Interfaces. No dependencies.

- [ ] **Step 5: Build and run checker**

```powershell
G:\Python313\python.exe herramientas\build_site.py
G:\Python313\python.exe herramientas\check_site.py --root .
```

Expected: home exists, checker passes for `index.html` (other pages may still be missing; use `--allow-missing` until Task 6).

- [ ] **Step 6: Commit**

```powershell
& $git add .
& $git commit -m "feat: add static site generator, design tokens and checker"
```

---

### Task 2: Home ES

**Files:**
- Create: `src/pages/home.es.html`
- Generate: `index.html`

- [ ] **Step 1: Write the home fragment**

Sections in order: nav/hero, spec table (8 rows, full document: PDF+LaTeX, 8 sections, 3+ alternatives, 15–25 days, design/documentation, no execution/signature, from USD 1.200, remote), “No vendo horas”, “IRD documenta. No ejecuta.”, sample preview (3 JPEG placeholders), method 4 steps, lab teaser (45%, October 2026), about teaser, pricing 3 cards + complex/monthly, FAQ 6, final CTA. Include the honesty line.

- [ ] **Step 2: Build and check**

```powershell
G:\Python313\python.exe herramientas\build_site.py
G:\Python313\python.exe herramientas\check_site.py --root . --allow-missing
```

Expected: no errors for `index.html`; no `10 a 15`, no `desde USD 450` in the spec table.

- [ ] **Step 3: Preview at 1440 and 390**

Use `tools.browser.preview({path:"index.html"})`, inspect:
- hero H1 visible, sheet does not overflow
- spec table readable at 390 (1 column)
- pricing cards stack
- CTA links resolve to `contacto.html`, `documento.html`
- keyboard focus visible

- [ ] **Step 4: Commit**

```powershell
& $git add index.html src/pages/home.es.html assets/css/style.css
& $git commit -m "feat: rebuild Spanish home"
```

---

### Task 3: Document ES + sample assets

**Files:**
- Create: `herramientas/build_samples.ps1`
- Create: `src/pages/documento.es.html`
- Generate: `documento.html`, `assets/docs/muestra-SOL-001.pdf`, `assets/img/muestra-p1.jpg` … `p3.jpg`

- [ ] **Step 1: Fix and compile the Spanish sample**

Copy the `.tex` + `LogoNegro.png` to `src/docs/build/es/`; remove `· ird.com.ar` from the cover; compile twice with `pdflatex`; render pages 1, 3, 4 with `pdftoppm -jpeg -r 120`; copy outputs. Expected: PDF 5 pages, cover has no `ird.com.ar`.

- [ ] **Step 2: Write the document page**

Sections: hero, anatomy 8 sections, sample 3 images + PDF download + “muestra abreviada de 5 páginas; un documento real tiene 18–25”, includes/excludes, validation-with-licensed-professional, process/timeline, full price table, payment/inflation terms, client inputs, FAQ, CTA.

- [ ] **Step 3: Build and check**

```powershell
G:\Python313\python.exe herramientas\build_site.py
G:\Python313\python.exe herramientas\check_site.py --root . --allow-missing
```

Expected: `documento.html` passes; PDF and 3 JPEGs exist; no `ird.com.ar` in PDF text or HTML.

- [ ] **Step 4: Preview and commit**

Check the PDF download link, image alt text, table at 390, and that the sample label is visible.

```powershell
& $git add documento.html src/pages/documento.es.html assets/docs assets/img herramientas/build_samples.ps1
& $git commit -m "feat: add document page and corrected sample"
```

---

### Task 4: Lab, About, Contact ES

**Files:**
- Create: `src/pages/laboratorio.es.html`, `src/pages/sobre-mi.es.html`, `src/pages/contacto.es.html`
- Generate: `laboratorio.html`, `sobre-mi.html`, `contacto.html`

- [ ] **Step 1: Lab page**

Biomass project: “Investigación propia · 45% · Rev. 0.3 · revisión octubre 2026”; problem, hypothesis, what is resolved, what is missing, next milestone without a fake date; CTA; “no es un caso de éxito”. No metrics.

- [ ] **Step 2: About page**

Ficha (role, UTN 3rd year, focus, languages, remote), why IRD exists, 4 principles, what IRD does/doesn’t do, validation workflow, monogram SB (no fake photo). Honesty line.

- [ ] **Step 3: Contact page**

Hero, form (name, email, country, company, problem, tried, timeline, budget, source, consent), email fallback, “what happens next” 24–48h, urgency note, scope note. Form has `data-endpoint=""` and `mailto:` fallback in `site.js`.

- [ ] **Step 4: Build, check, preview, commit**

```powershell
G:\Python313\python.exe herramientas\build_site.py
G:\Python313\python.exe herramientas\check_site.py --root . --allow-missing
```

Check form labels, keyboard order, `mailto:` build, no invented WhatsApp number.

```powershell
& $git add laboratorio.html sobre-mi.html contacto.html src/pages assets/js/site.js
& $git commit -m "feat: add lab, about and contact pages"
```

---

### Task 5: Terms and 404 ES

**Files:**
- Create: `src/pages/terminos.es.html`, `src/pages/404.es.html`
- Generate: `terminos.html`, `404.html`

- [ ] **Step 1: Terms**

14 sections from the spec: identification, object/scope, quotes, payment/MEP/IPC, deadlines, revisions, client responsibilities, IP/license, confidentiality, liability, cancellation, privacy (Ley 25.326), jurisdiction, contact. Version October 2026. No “no refunds for digital products” clause.

- [ ] **Step 2: 404**

Bilingual, links to ES/EN home, document and contact. Same visual system.

- [ ] **Step 3: Build, check, preview, commit**

```powershell
G:\Python313\python.exe herramientas\build_site.py
G:\Python313\python.exe herramientas\check_site.py --root . --allow-missing
```

```powershell
& $git add terminos.html 404.html src/pages/terminos.es.html src/pages/404.es.html
& $git commit -m "feat: add terms, privacy and bilingual 404"
```

---

### Task 6: English site + English sample

**Files:**
- Create: `src/pages/*.en.html` (6 fragments)
- Create: `src/docs/muestra-SOL-001-en.tex`
- Generate: `en/*.html`, `assets/docs/muestra-SOL-001-en.pdf`, `assets/img/muestra-en-p1.jpg` … `p3.jpg`

- [ ] **Step 1: Translate fragments**

Not literal. Key copy:
- H1: “You already have the problem. What’s missing is the document that solves it.”
- CTA: “Tell me what’s not working.”
- Nav: The document / Lab / About / Contact.
- Honesty: “IRD does not sign off on projects or replace a licensed engineer. It delivers technical documentation for a qualified professional to review and sign where required.”
- Prices with commas: USD 1,200; USD 450–500; USD 3,000. Dates in English.
- No “we” if one person.

- [ ] **Step 2: Translate and compile the sample**

Copy the Spanish `.tex`, switch babel to English, translate all headings/fields, remove `ird.com.ar`, compile twice, render pages 1, 3, 4. Label “Sample format. Illustrative content. Not a real case.”

- [ ] **Step 3: Build and run full checker**

```powershell
G:\Python313\python.exe herramientas\build_site.py
G:\Python313\python.exe herramientas\check_site.py --root .
```

Expected: all 13 pages pass; parity clean; no banned strings.

- [ ] **Step 4: Preview EN at 1440 and 390 + commit**

Check relative links (`../assets`, `../index.html`, `document.html`), hreflang, sample download, prices.

```powershell
& $git add en src/pages src/docs assets/docs assets/img
& $git commit -m "feat: add English site and sample document"
```

---

### Task 7: OG images, favicon, SEO

**Files:**
- Create: `assets/img/favicon.svg`
- Create: `src/og/og-es.html`, `src/og/og-en.html`
- Generate: `assets/img/og-ird-es.png`, `og-ird-en.png`, `sitemap.xml`, `robots.txt`

- [ ] **Step 1: Favicon**

64×64 SVG, paper background, black “IRD” monogram, no external fonts.

- [ ] **Step 2: OG images**

Create 1200×630 HTML pages using the design tokens, logo, headline and a small sheet. Open with `browser.preview`, screenshot the `#og` element at 1200×630, save as PNG. Verify dimensions and text legibility.

- [ ] **Step 3: Structured data**

Add JSON-LD `ProfessionalService` + `Person` + `Service` on home ES/EN and `FAQPage` where the FAQ is visible. No ratings/reviews.

- [ ] **Step 4: Sitemap/robots**

`build_site.py` writes `sitemap.xml` with all 12 indexable pages and `robots.txt` with the sitemap URL. 404 excluded from sitemap. No `ird.com.ar`.

- [ ] **Step 5: Check and commit**

```powershell
G:\Python313\python.exe herramientas\build_site.py
G:\Python313\python.exe herramientas\check_site.py --root .
```

```powershell
& $git add assets/img/favicon.svg assets/img/og-ird-es.png assets/img/og-ird-en.png sitemap.xml robots.txt src/og
& $git commit -m "feat: add social images, favicon and SEO files"
```

---

### Task 8: Archive old site, publish folder, final QA

**Files:**
- Create: `herramientas/publish.ps1`
- Move: old `soluciones.html`, `producto.html`, `asistente.html`, `admin.html`, `data.js`, `Problemas/`, old `style.css`, old index/terms/404 backups → `_legacy/`
- Generate: `dist/`

- [ ] **Step 1: Archive**

Move old files to `_legacy/`; keep copies in the baseline commit. Add `_legacy/README.md` (“not published; rollback material”). Do not delete `documentos/`, `Recursos/`, `herramientas/`.

- [ ] **Step 2: Publish script**

`publish.ps1` recreates `dist/`, copies the 7 public ES files, `en/`, `assets/`, `robots.txt`, `sitemap.xml`; asserts forbidden paths are absent.

- [ ] **Step 3: Run full QA**

```powershell
G:\Python313\python.exe herramientas\check_site.py --root .
G:\Python313\python.exe herramientas\check_site.py --root dist
powershell -ExecutionPolicy Bypass -File herramientas\publish.ps1
```

Manual:
- 320/360/390/768/1024/1440: no horizontal scroll
- keyboard: skip link, nav, FAQ, form
- `prefers-reduced-motion`: no reveal
- form: required validation + mailto opens
- PDF download + sample label
- all nav/footer/language links
- no `ird.com.ar` in `dist/` (HTML or PDF)

- [ ] **Step 4: Final commit**

```powershell
& $git add .
& $git commit -m "chore: archive old site and add publish pipeline"
```

---

## Acceptance Checklist

- [ ] 6 ES + 6 EN pages + bilingual 404, all generated and reachable.
- [ ] Every page has title, description, canonical, hreflang es-AR/en/x-default, OG.
- [ ] Home sells the full document (from USD 1,200, 15–25 days), not the diagnosis.
- [ ] Prices and payment terms consistent across home, document, terms, FAQ.
- [ ] Honesty line on home, document, about, terms.
- [ ] No invented cases, testimonials, metrics or dates.
- [ ] Sample PDF (ES/EN) has no `ird.com.ar`, is labeled illustrative, and is 5 pages with a note that real documents are 18–25.
- [ ] No old catalog/product/assistant/admin links.
- [ ] Mobile nav works without JS; form has fallback; links work from `file://`.
- [ ] `check_site.py --root .` and `--root dist` exit 0.
- [ ] `dist/` contains no source folders.
