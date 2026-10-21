from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = {
    ("documento", "es"): ("El documento de solución", "Qué recibís, cómo se ve y cuánto cuesta."),
    ("laboratorio", "es"): ("Laboratorio", "Investigación propia sobre valorización de biomasa."),
    ("sobre-mi", "es"): ("Sobre mí", "Documentación técnica, no firma de proyectos."),
    ("contacto", "es"): ("Contacto", "Contame qué problema técnico tenés."),
    ("terminos", "es"): ("Términos y privacidad", "Condiciones de contratación y uso."),
    ("home", "en"): ("The problem already exists. What is missing is the document that solves it.", "Technical solution documentation for industrial and process problems."),
    ("documento", "en"): ("The solution document", "What you receive, how it looks and what it costs."),
    ("laboratorio", "en"): ("Lab", "Independent research on biomass valorization."),
    ("sobre-mi", "en"): ("About", "Technical documentation, not project sign-off."),
    ("contacto", "en"): ("Contact", "Tell me what is not working."),
    ("terminos", "en"): ("Terms and privacy", "Engagement and use conditions."),
}

for (key, lang), (title, lead) in PAGES.items():
    home = "../index.html" if lang == "en" else "index.html"
    crumb = "Home" if lang == "en" else "Inicio"
    html = f'''<section class="page-hero">
  <div class="wrap page-hero-grid">
    <div>
      <div class="breadcrumb"><a href="{home}">{crumb}</a> / {title}</div>
      <h1>{title}</h1>
      <p class="lead">{lead}</p>
    </div>
  </div>
</section>
'''
    path = ROOT / "src" / "pages" / f"{key}.{lang}.html"
    path.write_text(html, encoding="utf-8", newline="\n")
    print(path.relative_to(ROOT))

error = '''<section class="error-page">
  <div class="wrap error-grid">
    <div><div class="error-code">404</div></div>
    <div>
      <div class="breadcrumb">Error / Error</div>
      <h1>Esta página no existe.<br><span lang="en">This page does not exist.</span></h1>
      <p>La URL cambió o el enlace está roto. <span lang="en">The URL changed or the link is broken.</span></p>
      <div class="error-links">
        <a href="index.html">Volver al inicio <span aria-hidden="true">→</span></a>
        <a href="en/index.html" hreflang="en" lang="en">Go to the English home <span aria-hidden="true">→</span></a>
        <a href="documento.html">Ver el documento <span aria-hidden="true">→</span></a>
        <a href="contacto.html">Contame tu problema <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>
'''
(ROOT / "src" / "pages" / "404.es.html").write_text(error, encoding="utf-8", newline="\n")
print("src/pages/404.es.html")
