/* IRD — comportamiento mínimo. El sitio se puede leer y navegar sin este archivo. */
(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;
  var lang = (root.getAttribute('lang') || 'es').toLowerCase();
  var isEn = lang.indexOf('en') === 0;

  /* Año actual en el pie. */
  doc.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  /* Menú móvil: <details> funciona sin JS; esto agrega cierre y foco. */
  var menu = doc.querySelector('.menu');
  if (menu) {
    var summary = menu.querySelector('summary');
    menu.addEventListener('toggle', function () {
      doc.body.classList.toggle('menu-open', menu.open);
      if (!menu.open) {
        doc.body.classList.remove('menu-open');
      }
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        menu.open = false;
      });
    });
    doc.addEventListener('click', function (event) {
      if (menu.open && !menu.contains(event.target)) {
        menu.open = false;
      }
    });
    doc.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menu.open) {
        menu.open = false;
        if (summary) summary.focus();
      }
    });
  }

  /* Aparición suave. Sin JS, .reveal es visible por defecto. */
  var reveals = doc.querySelectorAll('.reveal');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reveals.length) {
    if (!('IntersectionObserver' in window) || reduce) {
      reveals.forEach(function (el) { el.classList.add('is-visible'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
      reveals.forEach(function (el) { io.observe(el); });
    }
  }

  /* Formulario de contacto: mailto como fallback, endpoint opcional. */
  var form = doc.querySelector('[data-contact-form]');
  if (!form) return;

  var status = form.querySelector('.form-status');
  var submit = form.querySelector('[type="submit"]');

  var messages = isEn
    ? {
        required: 'This field is required.',
        email: 'Enter a valid email address.',
        consent: 'Please accept the privacy notice.',
        sending: 'Sending…',
        mailto: 'Your email client should open with the message ready. If it does not, write to sebabergesio472@gmail.com.',
        sent: 'Message sent. I will reply within 24–48 business hours.',
        error: 'Something went wrong. Please write to sebabergesio472@gmail.com.'
      }
    : {
        required: 'Este campo es obligatorio.',
        email: 'Ingresá un email válido.',
        consent: 'Aceptá el aviso de privacidad para continuar.',
        sending: 'Enviando…',
        mailto: 'Se abrió tu cliente de correo con el mensaje listo. Si no abre, escribime a sebabergesio472@gmail.com.',
        sent: 'Mensaje enviado. Respondo en 24–48 horas hábiles.',
        error: 'Algo falló. Escribime directamente a sebabergesio472@gmail.com.'
      };

  function fieldWrap(input) {
    return input.closest('.field') || input.closest('.checkbox') || input.parentElement;
  }

  function errorBox(input) {
    var wrap = fieldWrap(input);
    return wrap ? wrap.querySelector('.field-error') : null;
  }

  function setError(input, message) {
    var box = errorBox(input);
    if (message) {
      input.setAttribute('aria-invalid', 'true');
      if (box) {
        box.textContent = message;
        box.hidden = false;
      }
    } else {
      input.removeAttribute('aria-invalid');
      if (box) {
        box.textContent = '';
        box.hidden = true;
      }
    }
  }

  function clearStatus() {
    if (!status) return;
    status.className = 'form-status';
    status.textContent = '';
  }

  function showStatus(message, kind) {
    if (!status) return;
    status.textContent = message;
    status.className = 'form-status ' + kind;
  }

  function validate() {
    var ok = true;
    var firstInvalid = null;

    form.querySelectorAll('[required]').forEach(function (input) {
      var value = (input.value || '').trim();
      var valid = input.type === 'checkbox' ? input.checked : value.length > 0;
      if (input.type === 'email' && valid) {
        valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
      }
      if (!valid) {
        ok = false;
        var msg = input.type === 'email' ? messages.email : (input.type === 'checkbox' ? messages.consent : messages.required);
        setError(input, msg);
        if (!firstInvalid) firstInvalid = input;
      } else {
        setError(input, '');
      }
    });

    if (firstInvalid) {
      firstInvalid.focus();
      firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    return ok;
  }

  form.addEventListener('input', function (event) {
    var target = event.target;
    if (target && target.matches('input, textarea, select')) {
      setError(target, '');
      clearStatus();
    }
  });

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    clearStatus();

    if (form.querySelector('[name="website"]') && form.querySelector('[name="website"]').value) {
      return;
    }

    if (!validate()) {
      showStatus(isEn ? 'Check the highlighted fields.' : 'Revisá los campos marcados.', 'error');
      return;
    }

    var data = new FormData(form);
    var name = String(data.get('name') || '').trim();
    var email = String(data.get('email') || '').trim();
    var lines = [];
    var labels = isEn
      ? {
          name: 'Name', email: 'Email', country: 'Country', company: 'Company',
          problem: 'Problem', tried: 'What has been tried', timeline: 'Timeline',
          budget: 'Budget', source: 'How they found IRD', consent: 'Privacy notice accepted'
        }
      : {
          name: 'Nombre', email: 'Email', country: 'País', company: 'Empresa',
          problem: 'Problema', tried: 'Qué se probó', timeline: 'Plazo',
          budget: 'Presupuesto', source: 'Cómo llegó a IRD', consent: 'Aviso de privacidad aceptado'
        };

    Object.keys(labels).forEach(function (key) {
      var value = key === 'consent'
        ? (data.get('consent') ? (isEn ? 'Yes' : 'Sí') : (isEn ? 'No' : 'No'))
        : String(data.get(key) || '').trim();
      if (value) lines.push(labels[key] + ': ' + value);
    });

    var subject = (isEn ? 'IRD inquiry — ' : 'Consulta IRD — ') + name;
    var body = lines.join('\n');
    var endpoint = (form.getAttribute('data-endpoint') || '').trim();

    if (endpoint) {
      if (submit) submit.disabled = true;
      showStatus(messages.sending, 'ok');
      fetch(endpoint, {
        method: 'POST',
        body: data,
        headers: { Accept: 'application/json' }
      }).then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        showStatus(messages.sent, 'ok');
        form.reset();
      }).catch(function () {
        showStatus(messages.error, 'error');
      }).finally(function () {
        if (submit) submit.disabled = false;
      });
      return;
    }

    var mailto = 'mailto:sebabergesio472@gmail.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    showStatus(messages.mailto, 'ok');
    window.location.href = mailto;
  });
})();
