/* IRD — Cotización MEP en vivo para mostrar precios en ARS.
   Fuente: dolarapi.com (dólar bolsa / MEP, campo "venta").
   Los precios en USD son el ancla y siguen visibles sin JavaScript o sin red. */
(function () {
  'use strict';

  var ENDPOINT = 'https://dolarapi.com/v1/dolares/bolsa';
  var MARKUP = 1.05;                 /* Recargo por cobro en pesos. */
  var CACHE_KEY = 'ird.mep.v1';
  var CACHE_TTL = 10 * 60 * 1000;    /* 10 minutos. */
  var TIMEOUT = 8000;

  var doc = document;
  var lang = (doc.documentElement.getAttribute('lang') || 'es').toLowerCase();
  var isEn = lang.indexOf('en') === 0;
  var slots = Array.prototype.slice.call(doc.querySelectorAll('[data-price-ars]'));
  var notes = Array.prototype.slice.call(doc.querySelectorAll('[data-rate-note]'));
  if (!slots.length && !notes.length) return;

  var locale = isEn ? 'en-US' : 'es-AR';
  var nf0 = new Intl.NumberFormat(locale, { maximumFractionDigits: 0 });
  var nf2 = new Intl.NumberFormat(locale, { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  function parseUsd(raw) {
    var text = String(raw || '').trim();
    if (!text) return null;
    var from = /\+$/.test(text);
    var parts = text.replace(/\+$/, '').split('-');
    var values = [];
    for (var i = 0; i < parts.length; i++) {
      var n = Number(parts[i]);
      if (!isFinite(n) || n <= 0) return null;
      values.push(n);
    }
    return values.length ? { values: values, from: from } : null;
  }

  function arsAmount(usd, rate) {
    return Math.round((usd * rate * MARKUP) / 1000) * 1000;
  }

  function renderSlot(el, rate) {
    var parsed = parseUsd(el.getAttribute('data-usd'));
    if (!parsed) {
      el.textContent = '';
      return;
    }
    var numbers = parsed.values.map(function (usd) {
      return nf0.format(arsAmount(usd, rate));
    });
    var text = 'ARS ' + numbers.join(' – ');
    if (parsed.from || el.hasAttribute('data-usd-from')) {
      text = (isEn ? 'From ' : 'Desde ') + text;
    }
    if (el.hasAttribute('data-usd-month')) {
      text += isEn ? ' /month' : ' /mes';
    }
    el.textContent = text;
    el.setAttribute('data-state', 'ok');
  }

  function formatWhen(iso) {
    var when = iso ? new Date(iso) : new Date();
    if (isNaN(when.getTime())) when = new Date();
    try {
      return when.toLocaleString(locale, {
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit', hour12: false
      });
    } catch (err) {
      return when.toISOString().slice(0, 16).replace('T', ' ');
    }
  }

  function renderNote(rate, iso, stale) {
    var text = isEn
      ? 'MEP sell rate: ARS ' + nf2.format(rate) + ' per USD 1 · source: dolarapi.com · updated ' + formatWhen(iso) +
        '. ARS amounts include +5% and are estimates until payment.' + (stale ? ' (last available rate)' : '')
      : 'Cotización MEP venta: ARS ' + nf2.format(rate) + ' por USD 1 · fuente: dolarapi.com · actualizada ' + formatWhen(iso) +
        '. Los montos en ARS incluyen +5% y son estimativos hasta el pago.' + (stale ? ' (última cotización disponible)' : '');
    notes.forEach(function (el) {
      el.textContent = text;
      el.setAttribute('data-state', stale ? 'stale' : 'ok');
    });
  }

  function renderError() {
    var text = isEn
      ? 'Live MEP rate unavailable right now. Check dolarapi.com. ARS amounts could not be calculated.'
      : 'Cotización MEP no disponible en este momento. Consultá dolarapi.com. No se pudieron calcular los montos en ARS.';
    notes.forEach(function (el) {
      el.textContent = text;
      el.setAttribute('data-state', 'error');
    });
  }

  function apply(rate, iso, stale) {
    slots.forEach(function (el) { renderSlot(el, rate); });
    renderNote(rate, iso, stale);
  }

  function readCache() {
    try {
      var data = JSON.parse(window.localStorage.getItem(CACHE_KEY) || 'null');
      if (!data || !isFinite(data.rate) || data.rate <= 0) return null;
      return data;
    } catch (err) {
      return null;
    }
  }

  function writeCache(rate, iso) {
    try {
      window.localStorage.setItem(CACHE_KEY, JSON.stringify({ rate: rate, iso: iso, ts: Date.now() }));
    } catch (err) { /* almacenamiento no disponible */ }
  }

  function fetchRate() {
    return new Promise(function (resolve, reject) {
      var controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
      var timer = setTimeout(function () {
        if (controller) controller.abort();
        reject(new Error('timeout'));
      }, TIMEOUT);
      fetch(ENDPOINT, { cache: 'no-store', signal: controller ? controller.signal : undefined })
        .then(function (response) {
          if (!response.ok) throw new Error('HTTP ' + response.status);
          return response.json();
        })
        .then(function (data) {
          clearTimeout(timer);
          var rate = Number(data && data.venta);
          if (!isFinite(rate) || rate <= 0) throw new Error('cotización inválida');
          resolve({ rate: rate, iso: data.fechaActualizacion || '' });
        })
        .catch(function (err) {
          clearTimeout(timer);
          reject(err);
        });
    });
  }

  var cached = readCache();
  if (cached && Date.now() - cached.ts < CACHE_TTL) {
    apply(cached.rate, cached.iso, false);
    return;
  }
  if (cached) {
    apply(cached.rate, cached.iso, true);
  }

  fetchRate()
    .then(function (data) {
      writeCache(data.rate, data.iso);
      apply(data.rate, data.iso, false);
    })
    .catch(function () {
      if (!cached) renderError();
    });
})();
