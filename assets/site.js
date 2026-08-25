document.addEventListener('DOMContentLoaded', function(){

  // Mobile hamburger menu toggle
  var navToggle = document.getElementById('navToggle');
  var navEl = document.querySelector('.nav');
  if(navToggle && navEl){
    navToggle.addEventListener('click', function(){
      var isOpen = navEl.classList.toggle('mobile-open');
      navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }

  // Mobile mega-menu toggle (desktop uses hover via CSS)
  document.querySelectorAll('.nav-item > .nav-trigger').forEach(function(btn){
    btn.addEventListener('click', function(){
      var item = btn.closest('.nav-item');
      var isOpen = item.classList.contains('open');
      document.querySelectorAll('.nav-item.open').forEach(function(i){ i.classList.remove('open'); });
      if(!isOpen){
        item.classList.add('open');
        btn.setAttribute('aria-expanded','true');
      } else {
        btn.setAttribute('aria-expanded','false');
      }
    });
  });

  // Hero search tabs (Residential / Commercial)
  var heroSearchMode = 'res';
  document.querySelectorAll('.search-tab').forEach(function(tab){
    tab.addEventListener('click', function(){
      document.querySelectorAll('.search-tab').forEach(function(t){ t.classList.remove('active'); });
      tab.classList.add('active');
      heroSearchMode = tab.dataset.tab;
    });
  });

  // Any [data-realtor-search] control deep-links to Realtor.ca, centered on the chosen area
  document.querySelectorAll('[data-realtor-search]').forEach(function(btn){
    btn.addEventListener('click', function(){
      var selectId = btn.getAttribute('data-realtor-search');
      var select = selectId ? document.getElementById(selectId) : null;
      var coords = ((select && select.value) || '49.1913,-122.8490').split(',');
      var lat = parseFloat(coords[0]), lng = parseFloat(coords[1]);
      var dLat = 0.09, dLng = 0.14;
      var params = new URLSearchParams({
        ZoomLevel: '12',
        Center: lat + ',' + lng,
        LatitudeMax: (lat + dLat).toFixed(6),
        LongitudeMax: (lng + dLng).toFixed(6),
        LatitudeMin: (lat - dLat).toFixed(6),
        LongitudeMin: (lng - dLng).toFixed(6),
        PropertySearchTypeId: heroSearchMode === 'com' ? '3' : '0'
      });
      window.open('https://www.realtor.ca/map#' + params.toString(), '_blank', 'noopener');
    });
  });

  // FAQ accordions
  document.querySelectorAll('.faq-item').forEach(function(item){
    var q = item.querySelector('.faq-q');
    var a = item.querySelector('.faq-a');
    if(!q || !a) return;
    q.addEventListener('click', function(){
      var isOpen = item.classList.contains('open');
      item.closest('.faq').querySelectorAll('.faq-item.open').forEach(function(i){
        i.classList.remove('open');
        i.querySelector('.faq-a').style.maxHeight = null;
      });
      if(!isOpen){
        item.classList.add('open');
        a.style.maxHeight = a.scrollHeight + 'px';
      }
    });
  });

  // Lead forms (Formspree) — intercept submit, POST via fetch, swap in a
  // real success message instead of a page reload
  document.querySelectorAll('form[data-lead-form]').forEach(function(form){
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      var errorEl = form.querySelector('.form-error');
      var btnText = btn ? btn.textContent : '';
      if(errorEl) errorEl.hidden = true;
      if(btn){ btn.disabled = true; btn.textContent = 'Sending...'; }

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      }).then(function(res){
        if(!res.ok) throw new Error('bad status');
        form.innerHTML = '<div class="form-success"><strong>Message sent.</strong><span>Thanks — Manan will be in touch shortly.</span></div>';
      }).catch(function(){
        if(btn){ btn.disabled = false; btn.textContent = btnText; }
        if(errorEl) errorEl.hidden = false;
      });
    });
  });

  // Mortgage calculator
  var calc = document.getElementById('mortgageCalc');
  if(calc){
    var priceEl = document.getElementById('calcPrice');
    var downEl = document.getElementById('calcDown');
    var rateEl = document.getElementById('calcRate');
    var amortEl = document.getElementById('calcAmort');
    var outEl = document.getElementById('calcResult');
    var noteEl = document.getElementById('calcResultNote');
    var ctaEl = document.getElementById('calcCta');

    function recalc(){
      var price = parseFloat(priceEl.value) || 0;
      var downPct = parseFloat(downEl.value) || 0;
      var rate = parseFloat(rateEl.value) || 0;
      var years = parseFloat(amortEl.value) || 25;

      var downAmt = price * (downPct / 100);
      var principal = Math.max(price - downAmt, 0);
      var monthlyRate = (rate / 100) / 12;
      var n = years * 12;

      var payment = 0;
      if(principal > 0 && n > 0){
        if(monthlyRate === 0){
          payment = principal / n;
        } else {
          payment = principal * (monthlyRate * Math.pow(1 + monthlyRate, n)) / (Math.pow(1 + monthlyRate, n) - 1);
        }
      }
      var paymentStr = '~$' + Math.round(payment).toLocaleString('en-CA');
      outEl.textContent = paymentStr;
      noteEl.textContent = years + '-year amortization at ' + rate.toFixed(2) + '%';

      if(ctaEl){
        var msg = "Hi Manan, I estimated " + paymentStr + "/mo on a $" + Math.round(price).toLocaleString('en-CA') +
          " purchase (" + downPct + "% down, " + rate.toFixed(2) + "%, " + years + "yr) — can we talk?";
        ctaEl.href = 'sms:+16047279542?body=' + encodeURIComponent(msg);
      }
    }

    [priceEl, downEl, rateEl, amortEl].forEach(function(el){
      if(el) el.addEventListener('input', recalc);
    });
    recalc();
  }

});
