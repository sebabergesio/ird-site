# Rediseño del sitio de IRD — Documento de diseño

**Fecha:** 21 de octubre de 2026
**Estado:** Borrador para aprobación
**Alcance:** Sitio completo en español e inglés. 6 páginas por idioma + 404 bilingüe. Sin e-commerce.
**Autor:** Sebastián Bergesio / IRD

---

## 1. Resumen

IRD vende un documento técnico, no horas ni ejecución. El sitio actual no lo muestra: el catálogo está vacío, las tarjetas son texto genérico, hay una página de producto duplicada con un checkout que no existe y el proyecto de biomasa se presenta como si fuera un producto terminado.

Este rediseño convierte la web en una sola pieza: explicar el problema, mostrar el documento, probar que el formato es real y llevar a una consulta. La dirección visual es **"plano técnico"**: papel, grilla, tipografía monoespaciada, cajetín y una hoja A4 como objeto central. La **tabla de especificaciones de la ficha industrial** aporta los datos duros arriba del pliegue.

El modelo de negocio es simple: **un documento completo por mes (~USD 1.300) cubre el objetivo de ARS 1.500.000**. El sitio no necesita volumen; necesita calificar.

---

## 2. Por qué

- El catálogo vacío es peor que no tener catálogo: comunica que no hay trabajo.
- Las tarjetas de texto no prueban nada. El activo real es el PDF de muestra.
- "No somos una consultora / no somos una constructora" aparece tarde y en negativo. Hay que decirlo arriba y en positivo: **IRD documenta. No ejecuta.**
- El proyecto de biomasa al 45% es investigación, no un caso de éxito. Hay que rotularlo.
- No hay versión en inglés; un cliente del exterior no puede evaluar el servicio.
- No hay precios ni condiciones de pago; el cliente no sabe si puede pagarlo.
- El sitio no está desplegado. El rediseño incluye publicación, dominio y correo profesional.

---

## 3. Objetivos y no-objetivos

### Objetivos

1. Que un visitante entienda en 10 segundos qué se vende, para quién y cuánto cuesta.
2. Que el documento de muestra sea la prueba central de credibilidad.
3. Que la consulta llegue con contexto suficiente para cotizar sin diez idas y vueltas.
4. Que el sitio se vea como el trabajo que entrega: preciso, sobrio, verificable.
5. Que funcione en español e inglés, para clientes de todo el país y del exterior.
6. Que se pueda editar a mano, sin framework ni build obligatorio.

### No-objetivos

- Carrito, checkout, suscripciones automáticas.
- CMS, blog con comentarios, login de clientes.
- Chatbot o asistente de IA.
- Portfolio inventado, testimonios inventados, casos ficticios.
- Rediseño del logo o de la identidad del PDF.
- Posicionarse como ingeniero matriculado, consultora o constructora.

### Anti-objetivos de mensaje

- "Soluciones integrales", "sinergias", "transformación digital".
- "Somos líderes", "más de X años", "clientes satisfechos" (no hay evidencia).
- "Ingeniería de precisión" o cualquier promesa de resultado de ejecución.

---

## 4. Público

### Primario (Argentina)

- Dueño o gerente de PyME industrial (alimentos, metalmecánica, madera, agro) con un cuello de botella, una idea de producto o una inversión que no sabe cómo evaluar.
- Emprendedor con un producto físico que necesita un documento para un socio, un banco, un municipio o un taller.
- Estudio de ingeniería o arquitectura que necesita documentación de respaldo para un proyecto.

### Secundario (exterior)

- Pequeños fabricantes, startups de hardware y ONG que necesitan un estudio técnico acotado y remoto, en inglés, con precio en USD.

### No es para

- Quien busca ejecución, dirección de obra, prototipos o firma de ingeniero.
- Quien busca el CAD más barato por hora.
- Quien no puede aportar datos mínimos del problema.

### Trabajos a resolver (JTBD)

- "Tengo una idea y no sé si es viable."
- "Tengo un problema y no sé la causa."
- "Necesito comparar alternativas con números, no con opiniones."
- "Necesito un documento que otro pueda revisar, firmar o ejecutar."

---

## 5. Posicionamiento y mensaje

**Una línea:** IRD convierte un problema técnico en un documento de solución con alternativas, números y límites.

**Qué es:** estudio de documentación técnica. Analiza, compara, documenta. No ejecuta, no prototipa, no firma.

**Por qué confiar (sin portfolio):**

- El documento de muestra es real y se puede descargar.
- La estructura es fija y pública (8 secciones).
- Los límites están escritos.
- El proceso es explícito: consulta → alcance → documento → revisión.
- La validación por un profesional matriculado es parte del flujo, no letra chica.

**Frase de honestidad obligatoria** (home, documento, sobre mí y términos):

> IRD no firma proyectos ni reemplaza a un ingeniero matriculado. Entrega documentación técnica para que un profesional habilitado la valide y la firme cuando corresponda.

**Tono:** directo, técnico, sin adornos. Voseo argentino en español; inglés neutro y profesional. Sin signos de admiración. Sin promesas de resultados.

**Mensajes por audiencia:**

- PyME: "No pierdas plata probando. Compará alternativas antes de invertir."
- Emprendedor: "Tu idea necesita un documento, no una corazonada."
- Estudio: "Te ordeno la documentación para que la revisión y la firma sean rápidas."
- Exterior: "Remote technical documentation. Fixed scope, fixed price."

---

## 6. Oferta, precios e inflación

### Escalera de productos

| Producto | Precio | Horas | Plazo | Qué incluye |
|---|---:|---:|---|---|
| Consulta | USD 80 | 1 | 48–72 h | Videollamada, diagnóstico inicial, se descuenta del proyecto |
| Diagnóstico express | USD 450–500 | 12–16 | 7–10 días | 1 problema, 3 alternativas, 8–12 páginas |
| Documento completo | USD 1.200–1.400 | 28–36 | 15–25 días | 8 secciones, 18–25 páginas, 2 revisiones, ES o EN |
| Proyecto complejo | desde USD 3.000 | 60–100 | 4–8 semanas | Varias líneas, relevamiento, iteración |
| Acompañamiento mensual | USD 300 | 6–8 | mensual | Revisión de documentación y consultas |

**Piso absoluto:** USD 450 por entregable. La consulta de USD 80 es el único producto por debajo y se descuenta si avanza el proyecto. No hay descuentos por "ser nuevo".

**Por qué:** con 60 horas facturables por mes y un costo de vida de ~ARS 1.440.000, el costo por hora es ~ARS 24.000 (USD 15). Con un margen del 30%, la tarifa mínima es USD 22/h. El mercado paga USD 28–35/h (Upwork) y un informe técnico breve en Argentina arranca en USD 400 (GEXPLO, 2026). El documento completo a USD 1.300 equivale a ~USD 38/h.

### Modelo mensual

- 1 documento completo = **ARS ~2,05 M** (MEP 1.575).
- Objetivo de ingresos: **ARS 1.500.000/mes**.
- 2 diagnósticos = ARS 1,42 M: no alcanzan.
- 1 documento completo por mes alcanza y deja margen.

**Consecuencia para el sitio:** la home y el sitio entero deben vender el **documento completo**, no el diagnóstico barato. El diagnóstico es una puerta de entrada, no el negocio.

### Inflación y moneda

- Precio ancla en **USD**; cobro en ARS al **MEP del día + 5%**.
- Presupuesto válido **7 días**.
- Saldos impagos se ajustan por **IPC (INDEC)** desde la fecha del presupuesto hasta el pago.
- Revisión trimestral: si el IPC acumulado supera 10%, subir el precio en USD un 5%; si el MEP se mueve más de 15%, actualizar la lista.
- **50% adelantado, 50% contra entrega.** Proyectos de más de 30 días: 40/30/30.
- Monotributo: recategorizar según facturación.

**Qué se muestra en el sitio:** la ficha de la home describe el **documento completo** ("desde USD 1.200", 15–25 días). La escalera completa —consulta USD 80, diagnóstico desde USD 450, documento desde USD 1.200, complejo desde USD 3.000— aparece en `/documento` y en la sección de precios de la home. Condiciones de pago en `/documento` y `/terminos`. Nunca un precio cerrado sin alcance.

---

## 7. Arquitectura del sitio

### Español (raíz)

| URL | Página | Título |
|---|---|---|
| `/` | Home | IRD · Documentación técnica para resolver problemas |
| `/documento.html` | El documento | El documento de solución |
| `/laboratorio.html` | Laboratorio | Laboratorio · Investigación propia |
| `/sobre-mi.html` | Sobre mí | Sebastián Bergesio |
| `/contacto.html` | Contacto | Contame tu problema |
| `/terminos.html` | Términos y privacidad | Términos y condiciones |
| `/404.html` | 404 | Página no encontrada |

### Inglés (`/en/`)

| URL | Página | Título |
|---|---|---|
| `/en/` | Home | IRD · Technical documentation for engineering problems |
| `/en/document.html` | The document | The solution document |
| `/en/lab.html` | Lab | Lab · Independent research |
| `/en/about.html` | About | Sebastián Bergesio |
| `/en/contact.html` | Contact | Tell me what's not working |
| `/en/terms.html` | Terms & privacy | Terms and conditions |

El 404 es único, bilingüe, en la raíz.

### Navegación

**ES:** El documento · Laboratorio · Sobre mí · [Contame tu problema]
**EN:** The document · Lab · About · [Tell me what's not working]

- Logo a la izquierda, vuelve a la home del idioma.
- Selector **ES / EN** que lleva a la página equivalente, no a la home.
- En móvil, menú desplegable con `<details>` (funciona sin JavaScript).
- El CTA del nav es el único botón sólido.

### Footer

- Logo + tagline.
- Navegación secundaria.
- Email y ubicación: Reconquista, Santa Fe, Argentina · Trabajo remoto.
- "Términos y privacidad" y selector de idioma.
- Copyright dinámico (año).
- Sin redes sociales hasta que existan. No inventar LinkedIn.

### Archivos que se retiran

`soluciones.html`, `producto.html`, `asistente.html`, `admin.html`, `data.js`, `Problemas/problema-001.html`, `style.css` viejo.

Se archivan en `_legacy/` (noindex, fuera de la publicación) durante la implementación. No se borran hasta que el sitio nuevo esté aprobado y probado. El sitio actual no está desplegado, así que no se necesitan redirecciones; si alguna URL vieja estuviera indexada, se agregan 301.

---

## 8. Páginas

### 8.1 Home `/`

**Objetivo:** entender la oferta, ver la prueba y escribir.

**Orden de secciones:**

1. **Nav** (sticky, fondo papel, borde inferior).
2. **Hero** — dos columnas.
   - Izquierda: eyebrow mono "Estudio técnico · Reconquista, Argentina · Trabajo remoto"; H1 **"El problema ya lo tenés. Falta el documento que lo resuelve."**; lead: "Analizo el problema, comparo alternativas con datos y normativa, y te entrego un documento técnico listo para que un profesional lo valide y tu equipo lo ejecute. Sin prototipos. Sin dirección de obra."; CTAs: **"Contame tu problema"** (sólido) y **"Ver un documento real →"** (texto).
   - Derecha: hoja A4 en HTML/CSS con el documento de muestra (código SOL-001, título "Optimización de procesos", sello **MUESTRA**). No es una captura: es HTML, nítido en cualquier pantalla.
3. **Ficha del servicio** — tabla de especificaciones (dirección C) a ancho completo, debajo del hero. Dos columnas de pares etiqueta/valor:
   - Entregable: PDF + fuente LaTeX
   - Estructura: 8 secciones fijas
   - Alternativas: mínimo 3, comparadas
   - Plazo: 15 a 25 días
   - Alcance: diseño y documentación
   - No incluye: ejecución y firma
   - Inversión: desde USD 1.200
   - Modalidad: remota, todo el país y el exterior
4. **"No vendo horas. Entrego un documento."** — introducción + 4 pasos de la estructura: 01 Problema y causa raíz; 02 Alternativas comparadas; 03 Solución recomendada; 04 Resultado y límites. Link a `/documento.html`.
5. **"IRD documenta. No ejecuta."** — dos columnas:
   - Lo que hago: analizar, comparar, documentar, entregar.
   - Lo que no hago: prototipos, ejecución, dirección de obra, firma profesional.
   - Bloque de honestidad sobre la validación por matriculado.
6. **El documento, en serio** — preview de 3 páginas reales del PDF (portada, resumen, alternativas) + lista de "qué recibís" + botón **"Descargar muestra en PDF"** + nota "Muestra de formato. Contenido ilustrativo."
7. **Método** — 4 pasos: 01 Consulta (1 h, USD 80, se descuenta); 02 Alcance y presupuesto (7 días de validez); 03 Investigación y documento (15–25 días); 04 Entrega y revisión (2 rondas incluidas).
8. **Laboratorio** — bloque con el proyecto de biomasa: "Investigación propia · 45% · Rev. 0.3", una línea honesta ("No es un caso de éxito. Es un proyecto abierto.") y link a `/laboratorio.html`.
9. **Sobre mí** — ficha corta: nombre, rol, UTN Reconquista, 3º año en curso, "documento, no firma". Link a `/sobre-mi.html`.
10. **Precios** — 3 tarjetas: Consulta USD 80; Diagnóstico express USD 450–500; Documento completo USD 1.200–1.400. Línea aparte: "Proyecto complejo desde USD 3.000" y "Acompañamiento mensual USD 300". Nota de moneda, validez y ajuste.
11. **FAQ** — 6 preguntas:
    - ¿Vos firmás el proyecto? (No; entrego para validar y firmar.)
    - ¿Hacés prototipos o ejecutás la obra? (No.)
    - ¿Qué necesitás de mí? (Datos, acceso al problema, un responsable, 2–3 h de entrevistas.)
    - ¿Cuánto tarda? (Diagnóstico express: 7–10 días. Documento completo: 15–25 días desde que recibo los datos.)
    - ¿Cómo se paga? (50/50, USD, ARS al MEP + 5%, presupuesto 7 días.)
    - ¿Trabajás con clientes del exterior? (Sí, en inglés y en USD.)
12. **CTA final** — "Contame qué se rompe, qué querés mejorar o qué no te cierra." + email + link a contacto.
13. **Footer.**

**Regla de oro:** el CTA "Contame tu problema" aparece en el nav, en el hero y al final. Nada más compite con él.

### 8.2 El documento `/documento.html`

**Objetivo:** que el cliente sepa exactamente qué compra y pida presupuesto.

**Secciones:**

1. Hero: "El documento de solución" + subtítulo "Qué recibís, cómo se ve y cuánto cuesta." + CTA de descarga de muestra.
2. **Anatomía:** las 8 secciones, una por una, con qué responde cada una:
   - 01 Resumen ejecutivo
   - 02 Problema detectado (descripción, causa raíz, datos, consecuencias)
   - 03 Alternativas evaluadas (costo, tiempo, riesgo, motivo de descarte)
   - 04 Solución recomendada (criterios, cálculo, implementación, esquemas)
   - 05 Resultado esperado (beneficio, supuestos)
   - 06 Qué NO incluye (límites)
   - 07 Condiciones de uso y licencia
   - 08 Anexos (fuentes, normativa, glosario)
3. **Muestra:** 3 páginas reales + botón "Descargar PDF (1,6 MB)" + aviso de contenido ilustrativo. Aclarar que la muestra está abreviada (5 páginas) y que un documento real desarrolla cada sección y suele tener 18–25 páginas.
4. **Qué incluye / qué no incluye:** dos columnas. Incluye: diagnóstico, 3+ alternativas, solución, resultado, anexos, PDF + fuente LaTeX, documento en español o inglés, 2 revisiones, llamada de traspaso. No incluye: prototipo, ejecución, dirección de obra, firma, ingeniería de detalle para fabricación, trámites y permisos, garantía de resultados de implementación.
5. **Cómo se valida:** explicar el paquete para el profesional matriculado. "El documento le ahorra al profesional reconstruir el problema; su trabajo es revisar, ajustar y firmar."
6. **Proceso y plazos:** consulta → propuesta → 50% → investigación → borrador → revisión → entrega final + 50%. Plazos desde la recepción de datos.
7. **Precios:** tabla completa con horas, páginas, plazo y para quién es cada producto. Incluye la consulta y el acompañamiento mensual. Nota de moneda e inflación.
8. **Qué necesito de vos:** datos, acceso, responsable, 2–3 h de entrevistas, decisiones de restricción.
9. **FAQ del documento:** ¿puedo pedir cambios? (2 rondas); ¿qué pasa si el alcance cambia? (se presupuesta); ¿quién es el dueño del documento? (licencia de uso, no reventa); ¿puedo publicarlo? (no sin autorización); ¿qué pasa si no hay datos? (se cotiza relevamiento aparte).
10. CTA.

### 8.3 Laboratorio `/laboratorio.html`

**Objetivo:** mostrar que hay investigación real, sin fingir un portfolio.

**Secciones:**

1. Hero: "El laboratorio" + "Investigación propia, sin cliente. Acá está lo que estoy aprendiendo y lo que todavía no sé."
2. **Proyecto 001 — Sistema modular de valorización de biomasa.**
   - Estado: "Investigación propia · 45% · Rev. 0.3".
   - Problema: residuos orgánicos (poda, aceite, cáscaras) sin valorización; costos de disposición y energía.
   - Hipótesis: módulos de recolección, densificación y valorización térmica; subproducto biochar.
   - Qué está resuelto: marco del problema, alternativas de densificación, requisitos normativos preliminares.
   - Qué falta: viabilidad técnica de prensas, balances de masa/energía, emisiones, costos.
   - Próximo hito (con fecha solo si está definida; no inventar una).
   - CTA: "Si este problema es tuyo, puedo convertirlo en un proyecto pagado." Link a contacto.
   - Aviso: "No es un caso de éxito ni un producto terminado."
3. **Cómo se convierte en proyecto:** 01 definición del alcance; 02 relevamiento y datos; 03 documento con alternativas y recomendación.
4. **Notas de laboratorio (opcional):** solo entradas reales, fechadas y firmadas. Si no hay, no se publica la sección. No inventar bitácora.
5. CTA.

### 8.4 Sobre mí `/sobre-mi.html`

**Objetivo:** poner cara, explicar el método y resolver la objeción "es un estudiante".

**Secciones:**

1. Hero: "Sebastián Bergesio" + "Fundador de IRD · Reconquista, Argentina".
2. Ficha: rol, formación (3º año Ingeniería Electromecánica, UTN Facultad Regional Reconquista, en curso), foco (diseño, documentación, análisis técnico), idiomas (español, inglés), modalidad (remota).
3. **Por qué existe IRD:** el espacio entre "tengo la idea" y "tengo el documento".
4. **Cómo trabajo:** 4 principios — el problema antes que la solución; alternativas antes que la opinión; supuestos declarados; límites explícitos.
5. **Lo que sí y lo que no:** documento, no firma; análisis, no ejecución; diseño, no prototipo.
6. **Validación profesional:** el flujo con el matriculado, explicado sin eufemismos.
7. Foto real si existe; si no, monograma "SB" y ficha técnica. No usar fotos de stock ni retratos generados.
8. CTA.

### 8.5 Contacto `/contacto.html`

**Objetivo:** recibir un brief útil sin fricción.

**Secciones:**

1. Hero: "Contame tu problema." + "No necesito un brief perfecto. Con estas preguntas alcanza para saber si puedo ayudarte."
2. Formulario:
   - Nombre (requerido)
   - Email (requerido)
   - País y ciudad
   - Empresa u organización (opcional)
   - ¿Qué problema querés resolver? (requerido, textarea)
   - ¿Qué probaste o qué restricciones tenés? (opcional)
   - Plazo (urgente / 1 mes / 2–3 meses / sin fecha)
   - Rango de inversión (a definir / <500 / 500–1.500 / 1.500–3.000 / >3.000 USD)
   - Cómo me encontraste (opcional)
   - Consentimiento de privacidad con link a términos.
   - Botón "Enviar consulta".
   - Honeypot antispam.
3. Alternativa directa: email y WhatsApp (si Sebastián decide publicar el número).
4. **Qué pasa después:** 1) leo y respondo en 24–48 h hábiles; 2) si hay encaje, consulta de 1 h (USD 80, se descuenta); 3) si no, te digo por qué.
5. **Si tu problema es urgente:** decilo en el mensaje; la urgencia afecta disponibilidad y precio.
6. Nota de alcance: no firma de ingeniero; documentación para validar.
7. Sin mapa falso, sin foto de oficina, sin promesas de respuesta inmediata.

**Implementación del formulario:** estático. Action configurable a un endpoint (Formspree/Web3Forms) con fallback `mailto:` si no hay endpoint. El sitio funciona sin backend. El endpoint se define antes de publicar; si no, el formulario arma el correo con los datos y abre el cliente de correo.

### 8.6 Términos y privacidad `/terminos.html`

**Objetivo:** condiciones claras, sin letra chica.

**Secciones:**

1. Identificación: Sebastián Alan Bergesio, IRD, Reconquista, Santa Fe, Argentina, email.
2. Objeto y alcance: documentación técnica; no ejecución, no firma, no prototipos.
3. Presupuesto y precios: USD, validez 7 días, alcance por escrito.
4. Forma de pago y actualización: 50/50, MEP + 5%, IPC, mora.
5. Plazos y entregas: desde la recepción de datos; hitos.
6. Revisiones y cambios de alcance: 2 rondas; cambios se presupuestan.
7. Responsabilidades del cliente: datos veraces, acceso, profesional matriculado para validar/firmar.
8. Propiedad intelectual y licencia: uso único, no reventa, no publicación sin autorización.
9. Confidencialidad.
10. Límite de responsabilidad: la implementación es del cliente; no garantía de resultados de ejecución.
11. Cancelación: trabajo hecho se factura; seña no reembolsable una vez iniciado.
12. Privacidad: datos del formulario, finalidad, retención, derechos (acceso, rectificación, supresión), no venta a terceros. Ley 25.326.
13. Ley aplicable y jurisdicción: Argentina, tribunales de Santa Fe.
14. Contacto.
15. Versión: octubre 2026.

**Nota interna:** el texto es una base; conviene que un abogado lo revise antes de publicar. No es asesoramiento legal.

### 8.7 404 `/404.html`

Bilingüe, en la raíz:

- "404 · Página no encontrada" / "Page not found".
- "La página que buscás no existe o cambió de lugar." / "The page you're looking for doesn't exist or has moved."
- Links: Home, El documento, Contacto / Home, The document, Contact.
- Mismo sistema visual. Sin chistes.

---

## 9. Sistema visual

### Dirección

**"Plano técnico"**: papel, grilla, tinta negra, reglas finas, tipografía monoespaciada para datos, hoja A4 como objeto. La sensación es de documento de trabajo, no de landing de agencia.

### Paleta

| Token | Valor | Uso |
|---|---|---|
| `--paper` | `#F1F0EA` | Fondo |
| `--paper-2` | `#E9E7DF` | Bloques alternos |
| `--ink` | `#111417` | Texto principal |
| `--muted` | `#5C6166` | Texto secundario (contraste 5,5:1) |
| `--line` | `rgba(17,20,23,.16)` | Reglas finas |
| `--line-strong` | `rgba(17,20,23,.38)` | Reglas de estructura |
| `--teal` | `#0B6B6B` | Acento técnico, links, reglas (contraste 5,5:1) |
| `--accent` | `#C2410C` | Botones y texto pequeño naranja (AA) |
| `--accent-bright` | `#D9480F` | Números y trazos grandes |
| `--white` | `#FFFFFF` | Hoja del documento |

**Nota de marca:** el cian `#00FFFF` del logo y del PDF no tiene contraste suficiente sobre papel. En pantalla se usa el teal `#0B6B6B` como equivalente. El naranja brillante se reserva para elementos grandes; el naranja de interfaz es `#C2410C` para cumplir AA. El logo no se modifica.

### Tipografía

- **Inter** 400/500/600/700/800 para texto y títulos.
- **IBM Plex Mono** 400/500/600 para etiquetas, códigos, tablas, botones y datos.
- H1: `clamp(38px, 5vw, 64px)`, line-height 1.02, letter-spacing -0.035em, peso 800.
- H2: `clamp(26px, 3vw, 40px)`, line-height 1.1, peso 800.
- Body: 16–17px, line-height 1.65.
- Mono: 10–12px, uppercase, letter-spacing .12–.16em.
- Sin fuentes decorativas. Sin cursivas salvo citas.

### Grilla y layout

- Ancho máximo 1180px; padding lateral 32px desktop, 20px móvil.
- Grilla de fondo de dos niveles: 120px y 24px, opacidad 3–5%. Se desactiva en móvil si genera ruido.
- Secciones: 80–100px de aire arriba y abajo en desktop; 56–64px en móvil.
- Todo borde recto. Sin `border-radius` salvo el sello y el favicon.
- Líneas de 1px; las estructurales de 2px en negro.

### Componentes

- **Nav sticky:** 76–82px, borde inferior, fondo papel. Logo 40–44px.
- **Botón sólido:** fondo `--accent`, texto blanco, mono 11px uppercase, padding 16×26, borde 1px. Hover: fondo transparente, texto `--accent`.
- **Botón fantasma:** borde 1px ink, fondo transparente. Hover: fondo ink, texto papel.
- **Link de texto:** subrayado 1px, con "→" en naranja.
- **Hoja A4:** fondo blanco, borde 1px, sombra desplazada 24px, cabecera mono con línea teal de 2px, sello "MUESTRA" rotado -6°.
- **Ficha del servicio:** tabla de 8 pares etiqueta/valor, borde 1px ink, encabezado mono "FICHA DEL SERVICIO · REV. 01". En desktop, 2 columnas de 4 filas; en móvil, 1 columna.
- **Banda de datos:** 4 celdas con números grandes (03+, 08, 100%, 00) y etiquetas mono. Opcional en la home después de la ficha.
- **Steps:** 4 columnas con borde superior, número mono naranja, título y texto. En móvil, 2×2 o 1 columna.
- **Tabla de precios:** 3 tarjetas con borde 1px, sin sombra, precio grande, lista de incluido, CTA. La del medio puede llevar fondo blanco y borde 2px.
- **FAQ:** `<details>` nativo, resumen con "+" que rota a "×", borde inferior. Sin JS.
- **Formulario:** labels mono arriba, inputs con borde 1px ink, fondo transparente, focus teal 2px. Sin placeholders como única etiqueta.
- **Footer:** borde superior 2px, 4 columnas en desktop, stack en móvil, mono 10px.

### Movimiento

- Reveal on scroll: opacidad 0→1, translateY 8px→0, 400ms, solo si `prefers-reduced-motion: no-preference`.
- Hover de botones: 150ms.
- Sin parallax, sin autoplay, sin animaciones de fondo.
- El menú móvil se abre/cierra con `<details>`; JS solo lo cierra al hacer clic en un link.

### Imágenes

- Logos SVG.
- Hoja del hero: HTML/CSS, no imagen.
- Preview del PDF: 3 páginas renderizadas a JPEG (120 dpi, ancho máximo 900px, calidad 82, <100KB cada una), lazy-load.
- OG image: 1200×630 PNG, generada desde una página HTML con el sistema visual. Una versión ES y una EN.
- Foto de Sebastián: solo real. Si no hay, monograma "SB" en la ficha. Nada de stock ni IA.
- Diagrama del laboratorio: SVG simple, opcional. Si no aporta, no se usa.

### Accesibilidad visual

- Contraste mínimo AA en texto normal.
- Naranja `#C2410C` para texto pequeño; `#D9480F` solo para display.
- Foco visible: 2px teal con offset 2px.
- No transmitir información solo por color.
- Tamaño de tap ≥44px.
- `prefers-reduced-motion` respetado.

---

## 10. Contenido y pruebas

### Documento de muestra

- Archivo: `documentos/ejemplo-SOL-001.pdf` (5 páginas, A4, 1,6 MB).
- Se copia a `assets/docs/muestra-SOL-001.pdf`.
- Se muestra con 3 páginas renderizadas (portada, resumen ejecutivo, alternativas).
- Rótulo visible: **"Muestra de formato. Contenido ilustrativo. No es un caso real."**
- El PDF conserva "PyME de ejemplo S.A." y "Cliente: PyME de ejemplo S.A."; no se presenta como cliente real.
- El botón de descarga no promete confidencialidad ni resultados.
- La muestra tiene 5 páginas porque el contenido es ilustrativo. Un documento real desarrolla cada sección y suele tener 18–25 páginas; la página lo aclara para que el tamaño de la muestra no se lea como el tamaño del entregable.
- **La portada del PDF actual dice `ird.com.ar`, que pertenece a otra empresa.** Antes de publicar, se corrige la plantilla (dominio nuevo o sin dominio) y se recompila la muestra; no se sube el PDF viejo.

### Versión en inglés de la muestra

- Se traduce el mismo contenido ilustrativo (no se inventa un caso nuevo) y se compila `ejemplo-SOL-001-en.pdf` con la plantilla LaTeX.
- Se generan 3 páginas JPEG para `/en/document.html` y la home en inglés.
- Se rotula igual: **"Sample format. Illustrative content. Not a real case."**
- El PDF en inglés y el español comparten estructura, datos y límites; solo cambia el idioma.
- Si la traducción del PDF no se puede compilar a tiempo, el sitio en inglés muestra la muestra en español con una nota explícita; no se publica una captura trucada.

### Proyecto de biomasa

- Se presenta como investigación propia, no como caso.
- Estado 45%, revisión octubre 2026; próximo hito sin fecha inventada (si Sebastián la define, se publica).
- "Qué falta" es obligatorio; no solo "qué está resuelto".
- Sin métricas inventadas de ahorro, emisiones o costos.
- Si el proyecto avanza, se actualiza la ficha; si se abandona, se dice.

### Pruebas sociales

- No hay testimonios ni logos de clientes. No se inventan.
- La prueba es el documento, la estructura, el método y la transparencia.
- Si en el futuro hay un cliente, se pide permiso escrito y se anonimiza si hace falta.

### Voz

- Español: voseo, frases cortas, verbos concretos. "Analizo", "entrego", "comparo". No "brindamos soluciones".
- Inglés: "I analyze", "I deliver". Sin "we" si es una sola persona. Sin "cutting-edge".
- Números siempre con unidad y fecha. "USD 1.300", "15 a 25 días", "octubre 2026".
- No usar "barato", "rápido" ni "garantizado" sin contexto.

### Legal y confidencialidad

- Términos reescritos para servicios, no para productos digitales.
- Se elimina la frase "no se realizan reembolsos una vez enviado el material" y se reemplaza por una política de cancelación justa.
- Se aclara que el documento no es un proyecto firmado ni reemplaza la revisión de un matriculado.
- Política de privacidad para el formulario.

---

## 11. Técnica

### Stack

- HTML5 estático, CSS y JavaScript sin dependencias.
- Sin framework, sin build obligatorio, sin npm.
- Google Fonts (Inter + IBM Plex Mono) con `preconnect` y `display=swap`. Si se quiere evitar el tercero, self-host de woff2 como optimización posterior.
- Un solo CSS: `assets/css/style.css`.
- Un solo JS: `assets/js/site.js`.
- Imágenes y PDF en `assets/`.

### Estructura de archivos

```
IRD/
  index.html
  documento.html
  laboratorio.html
  sobre-mi.html
  contacto.html
  terminos.html
  404.html
  en/
    index.html
    document.html
    lab.html
    about.html
    contact.html
    terms.html
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
  _legacy/          (no se publica)
  documentos/       (fuente, no se publica)
  Recursos/         (fuente, no se publica)
  herramientas/     (fuente, no se publica)
  docs/             (documentación, no se publica)
```

### Header y footer

- Se replican en cada página con un bloque canónico.
- Para evitar drift, la implementación puede generar los archivos una vez con un script local; el sitio publicado no depende del script.
- Cada página debe actualizar: `lang`, title, description, canonical, hreflang, OG, nav activo y selector de idioma.

### JavaScript

- Menú móvil: `<details>` nativo; JS cierra al hacer clic en un link.
- Reveal on scroll con `IntersectionObserver`; si no hay soporte, todo visible.
- Año del copyright.
- Formulario: validación básica, honeypot, fallback `mailto:`.
- Copiar email al portapapeles (opcional).
- Sin dependencias, <5KB.

### Formulario

- `action` configurable en `data-endpoint` (Formspree/Web3Forms) o `mailto:` si está vacío.
- Validación en cliente: nombre, email, mensaje, consentimiento.
- Mensaje de éxito inline; si usa `mailto:`, aviso de que se abrió el cliente de correo.
- Accesibilidad: labels, `aria-describedby` para errores, foco al primer error.
- Honeypot oculto; sin captcha visible.

### i18n

- Español en la raíz; inglés en `/en/`.
- `lang="es"` / `lang="en"`.
- `hreflang="es-AR"`, `hreflang="en"`, `hreflang="x-default"` (español).
- Selector de idioma a la página equivalente.
- Sin redirección automática por idioma del navegador (rompe SEO y control del usuario).
- Paridad de contenido: cada página ES tiene su EN y viceversa.

### SEO

- Title y meta description únicos por página e idioma.
- Canonical absoluto con el dominio final.
- OG/Twitter con imagen 1200×630 por idioma.
- `sitemap.xml` con todas las URLs y alternates.
- `robots.txt` con sitemap.
- Structured data: `ProfessionalService` + `Person` (fundador) + `Service` (documento) + `FAQPage` (home y documento).
- Sin `aggregateRating` ni `Review` inventados.
- URLs limpias y estables; `.html` es aceptable para un sitio estático.
- **Dominio:** `ird.com.ar` está registrado por otra empresa de servicios IT (verificado el 21/10/2026). No se usa. El dominio se define antes de publicar; candidatos a verificar: `ird.ar`, `ird.engineering`, `irdiseno.com.ar`, `ingenieriarapida.com.ar`. Mientras tanto, el código usa `https://ird.example` como placeholder y se reemplaza en un solo lugar.

### Rendimiento

- HTML <60KB por página.
- CSS <25KB, JS <5KB.
- Fuentes: solo los pesos usados.
- Imágenes con `width`/`height`, `loading="lazy"` debajo del pliegue.
- PDF fuera del critical path (solo se descarga al hacer clic).
- Sin librerías de terceros salvo Google Fonts.
- Objetivo: Lighthouse ≥90 performance, ≥95 accesibilidad y SEO en móvil.

### Compatibilidad

- Chrome/Edge, Firefox, Safari modernos.
- iOS Safari y Chrome Android.
- Sin Internet Explorer.
- `<details>`, grid y custom properties son la base; no hay polyfills.

### Publicación

- Hosting estático: Netlify, Vercel o Cloudflare Pages (free tier).
- Se publica solo la carpeta pública (`dist/` generada por copia), no `documentos/`, `Recursos/`, `herramientas/`, `_legacy/` ni `docs/`.
- HTTPS y dominio propio.
- `404.html` en la raíz para el fallback del host.
- Redirects 301 si se detectan URLs viejas indexadas.
- Analytics opcional, sin cookies (Plausible/Umami o el analytics del host). Sin banner si no hay cookies.
- Eventos: clic en CTA, descarga de muestra, envío de formulario, cambio de idioma.

---

## 12. Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| No hay portfolio | Baja confianza | Documento de muestra real + estructura pública + consulta paga |
| Es estudiante, no matriculado | Objeción de legitimidad | Frase explícita + flujo de validación + límites en términos |
| Laboratorio vacío o estancado | Parece abandono | Un proyecto honesto con fecha y próximo hito; sin bitácora inventada |
| Bilingüe se desincroniza | Mala experiencia/SEO | Checklist de paridad + hreflang + revisión antes de publicar |
| Inflación licúa precios | Margen | USD ancla + MEP + 5% + IPC + revisión trimestral |
| Falta de tráfico | Sin consultas | SEO + LinkedIn/outbound; el sitio no genera demanda solo |
| Cobro internacional | Fricción | Definir Wise/PayPal antes de publicar |
| Dominio/correo | Baja credibilidad | Comprar dominio y correo profesional antes de publicar |
| Términos incompletos | Riesgo legal | Revisión por abogado; base clara |
| Formulario sin backend | Consultas perdidas | Endpoint Formspree/Web3Forms + fallback mailto + email visible |

---

## 13. Decisiones abiertas (para Sebastián)

1. **Dominio y correo:** `ird.com.ar` no es tuyo: está ocupado por otra empresa de servicios IT. ¿Tenés otro dominio o compramos uno? Candidatos a verificar: `ird.ar`, `ird.engineering`, `irdiseno.com.ar`, `ingenieriarapida.com.ar`. El correo profesional depende de esa decisión; hasta entonces, Gmail.
2. **Cobro internacional:** ¿Wise, PayPal, Stripe u otro? ¿Ya tenés cuenta?
3. **WhatsApp:** ¿publicamos tu número en la página de contacto?
4. **Foto:** ¿tenés una foto real para Sobre mí? Si no, usamos monograma.
5. **Precios públicos:** ¿OK con mostrar "desde USD 1.200" para el documento completo y la escalera con la consulta y el diagnóstico desde USD 450?
6. **Formulario:** ¿creás una cuenta gratis en Formspree/Web3Forms o preferís el fallback de correo?
7. **Hosting:** ¿Netlify, Vercel, Cloudflare Pages u otro? ¿Ya tenés dominio?
8. **LinkedIn:** ¿existe un perfil para enlazar? Si no, no se inventa.
9. **Términos:** ¿los revisa un abogado antes de publicar?

---

## 14. Criterios de aceptación

1. Existen las 6 páginas en español y las 6 en inglés, más el 404 bilingüe.
2. Cada página tiene `lang`, title, description, canonical, hreflang y OG correctos.
3. La home explica la oferta, el plazo y el precio del documento completo antes del primer scroll completo.
4. El documento de muestra (ES y EN) se descarga y está rotulado como muestra.
5. No hay casos, testimonios ni métricas inventadas.
6. La limitación "no firma / validar con matriculado" aparece en home, documento, sobre mí y términos.
7. La tabla de precios y las condiciones de moneda/inflación son visibles.
8. El sitio funciona sin JavaScript para navegar y leer; el formulario tiene fallback.
9. Responsive de 320px a 1440px sin scroll horizontal.
10. Contraste AA, foco visible, navegación por teclado, `prefers-reduced-motion`.
11. No hay links rotos ni imágenes faltantes.
12. El sitio se publica desde una carpeta pública sin archivos fuente.
13. Lighthouse ≥90 performance y ≥95 accesibilidad/SEO en móvil (o revisión manual equivalente).
14. El texto en inglés no parece traducción automática.

---

## 15. Fuera de alcance

- E-commerce, carrito, checkout, suscripciones.
- CMS o blog con flujo de publicación.
- Login de clientes o portal de proyectos.
- Chatbot/asistente.
- Panel de administración.
- Newsletter.
- Traducciones a otros idiomas.
- Rediseño de logo o plantilla LaTeX.
- Producción de casos de estudio nuevos.
- Campaña de marketing, SEO off-page o gestión de redes.
- Firma de proyectos por parte de IRD.

---

## 16. Resumen de la decisión

**Qué:** rediseño completo, estático, bilingüe, con el documento como prueba y la consulta como conversión.

**Por qué:** el sitio actual no muestra el trabajo real y no permite evaluar precio, alcance ni límites.

**Cómo:** dirección "plano técnico" + ficha de especificaciones, 6 páginas por idioma, documento de muestra, precios transparentes, lenguaje honesto sobre el rol del matriculado.

**Cuándo:** implementación después de aprobar este documento y resolver dominio, correo, cobro y formulario.

**Éxito:** una consulta calificada por mes que se convierta en un documento completo; el sitio como prueba de que IRD documenta en serio.
