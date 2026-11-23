// 스테가비전 사이트 공통 동작
(function () {
  // 모바일 메뉴
  var btn = document.querySelector('.menu-btn'), nav = document.querySelector('.nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // 홈 메인 슬라이드
  var slides = document.querySelectorAll('.hero-slide'), dots = document.querySelectorAll('.hero-dots button');
  if (slides.length > 1) {
    var cur = 0, timer;
    var show = function (i) {
      cur = (i + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.classList.toggle('on', k === cur); });
      dots.forEach(function (d, k) { d.classList.toggle('on', k === cur); });
    };
    var start = function () { clearInterval(timer); timer = setInterval(function () { show(cur + 1); }, 5000); };
    dots.forEach(function (d, k) { d.addEventListener('click', function () { show(k); start(); }); });
    start();
  }

  // 넘어가는 사진 줄 (응용분야, 특허증, 논문)
  function Carousel(el) {
    var view = el.querySelector('.car-view'), track = el.querySelector('.car-track');
    var real = Array.prototype.slice.call(track.children), n = real.length;
    var center = el.hasAttribute('data-center');
    var spec = (el.getAttribute('data-visible') || '4,3,2').split(',').map(Number);
    var auto = Number(el.getAttribute('data-auto') || 0);
    var idx = 0, w = 0, loop = false, timer = null, busy = false;
    function visible() { var W = window.innerWidth; return W <= 767 ? spec[2] : W <= 1100 ? spec[1] : spec[0]; }
    function build() {
      Array.prototype.slice.call(track.querySelectorAll('.car-clone')).forEach(function (c) { c.remove(); });
      var v = visible();
      loop = n > Math.floor(v);
      w = view.clientWidth / v;
      if (loop) {
        var before = document.createDocumentFragment(), after = document.createDocumentFragment();
        real.forEach(function (it) { var c = it.cloneNode(true); c.classList.add('car-clone'); c.setAttribute('aria-hidden', 'true'); before.appendChild(c); });
        real.forEach(function (it) { var c = it.cloneNode(true); c.classList.add('car-clone'); c.setAttribute('aria-hidden', 'true'); after.appendChild(c); });
        track.insertBefore(before, track.firstChild); track.appendChild(after);
        if (idx < n || idx >= 2 * n) idx = n + (((idx % n) + n) % n);
      } else { idx = 0; }
      Array.prototype.slice.call(track.children).forEach(function (it) { it.style.width = w + 'px'; });
      el.classList.toggle('car-static', !loop);
      place(false);
    }
    function place(anim) {
      track.style.transition = anim ? 'transform .7s cubic-bezier(.25,.8,.3,1)' : 'none';
      var off = loop ? idx * w - (center ? (view.clientWidth - w) / 2 : 0) : (center ? -(view.clientWidth - n * w) / 2 : 0);
      track.style.transform = 'translate3d(' + (-off) + 'px,0,0)';
      if (center) {
        var k = ((idx % n) + n) % n;
        Array.prototype.slice.call(track.children).forEach(function (it, i) { it.classList.toggle('is-center', loop ? i % n === k : false); });
      }
    }
    function go(d) {
      if (!loop || busy) return;
      busy = true; idx += d; place(true);
    }
    track.addEventListener('transitionend', function (e) {
      if (e.target !== track) return;
      busy = false;
      if (idx >= 2 * n) { idx -= n; place(false); } else if (idx < n) { idx += n; place(false); }
    });
    function start() { stop(); if (auto && loop) timer = setInterval(function () { go(1); }, auto); }
    function stop() { clearInterval(timer); }
    var prev = el.querySelector('.car-prev'), next = el.querySelector('.car-next');
    if (prev) prev.addEventListener('click', function () { go(-1); start(); });
    if (next) next.addEventListener('click', function () { go(1); start(); });
    el.addEventListener('mouseenter', stop); el.addEventListener('mouseleave', start);
    var x0 = null;
    view.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; stop(); }, { passive: true });
    view.addEventListener('touchend', function (e) {
      if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 40) go(dx < 0 ? 1 : -1); start();
    });
    var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { busy = false; build(); }, 150); });
    el._rebuild = function () { busy = false; build(); start(); };
    build(); start();
  }
  Array.prototype.slice.call(document.querySelectorAll('.carousel')).forEach(Carousel);

  // 특허 / 논문 탭
  var tabs = document.querySelectorAll('.tabs button');
  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      tabs.forEach(function (x) { x.classList.toggle('on', x === t); x.setAttribute('aria-selected', x === t ? 'true' : 'false'); });
      document.querySelectorAll('.cert-panel').forEach(function (p) {
        p.hidden = p.id !== t.getAttribute('data-panel');
        var c = p.querySelector('.carousel'); if (!p.hidden && c && c._rebuild) c._rebuild();
      });
    });
  });

  // 이미지 크게 보기
  var box = document.querySelector('.lightbox');
  if (box) {
    var big = box.querySelector('img');
    document.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('[data-zoom]') : null;
      if (!a) return;
      e.preventDefault();
      big.src = a.getAttribute('href');
      big.alt = a.querySelector('img') ? a.querySelector('img').alt : '';
      box.classList.add('on');
    });
    var close = function () { box.classList.remove('on'); big.removeAttribute('src'); };
    box.addEventListener('click', close);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }
})();
