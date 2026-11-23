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
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function Carousel(el) {
    var view = el.querySelector('.car-view'), track = el.querySelector('.car-track');
    var real = Array.prototype.slice.call(track.children), n = real.length;
    var center = el.hasAttribute('data-center');
    var spec = (el.getAttribute('data-visible') || '4,3,2').split(',').map(Number);
    var auto = Number(el.getAttribute('data-auto') || 0);
    var marquee = Number(el.getAttribute('data-marquee') || 0); // 사진 한 장이 지나가는 데 걸리는 초
    var off = 0, raf = null, last = 0, hold = false;
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
      el.classList.toggle('car-marquee', !!marquee && loop);
      if (marquee && loop) { off = n * w; track.style.transition = 'none'; draw(); return; }
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
    // 멈추지 않고 일정한 속도로 흘러가는 방식
    function draw() { track.style.transform = 'translate3d(' + (-off) + 'px,0,0)'; }
    function tick(t) {
      if (last && !hold && loop) {
        off += (w / (marquee * 1000)) * Math.min(t - last, 100);
        if (off >= 2 * n * w) off -= n * w;
        draw();
      }
      last = t; raf = requestAnimationFrame(tick);
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
    function start() {
      stop();
      if (marquee) { hold = false; if (!raf && !reduce) { last = 0; raf = requestAnimationFrame(tick); } return; }
      if (auto && loop) timer = setInterval(function () { go(1); }, auto);
    }
    function stop() { clearInterval(timer); if (marquee) hold = true; }
    var prev = el.querySelector('.car-prev'), next = el.querySelector('.car-next');
    if (prev) prev.addEventListener('click', function () { go(-1); start(); });
    if (next) next.addEventListener('click', function () { go(1); start(); });
    el.addEventListener('mouseenter', stop); el.addEventListener('mouseleave', start);
    var x0 = null;
    view.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; stop(); }, { passive: true });
    view.addEventListener('touchend', function (e) {
      if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (marquee && loop) { off += -dx; while (off < n * w) off += n * w; while (off >= 2 * n * w) off -= n * w; draw(); }
      else if (Math.abs(dx) > 40) go(dx < 0 ? 1 : -1);
      start();
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

  // 문의하기: 작성한 내용을 메일 작성 창으로 넘긴다
  var form = document.getElementById('inquiry');
  if (form) {
    var msg = document.getElementById('inquiry-msg');
    var to = (form.querySelector('.form-note a') || {}).textContent || '';
    var say = function (text, ok) { msg.textContent = text; msg.classList.toggle('ok', !!ok); };
    var collect = function () {
      var f = form.elements, bad = null;
      ['name', 'phone', 'message'].forEach(function (k) {
        var empty = !f[k].value.trim();
        f[k].classList.toggle('bad', empty);
        if (empty && !bad) bad = f[k];
      });
      if (bad) { say('성함, 연락처, 내용을 입력해 주세요.'); bad.focus(); return null; }
      return '회사명: ' + f.company.value.trim() + '\n성함: ' + f.name.value.trim() + '\n연락처: ' + f.phone.value.trim() +
        '\n이메일: ' + f.email.value.trim() + '\n\n문의 내용:\n' + f.message.value.trim() + '\n';
    };
    form.addEventListener('input', function (e) { if (e.target.classList) e.target.classList.remove('bad'); });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var body = collect(); if (!body) return;
      var who = form.elements.company.value.trim() || form.elements.name.value.trim();
      window.location.href = 'mailto:' + to + '?subject=' + encodeURIComponent('[스테가비전 문의] ' + who) + '&body=' + encodeURIComponent(body);
      say('메일 작성 창을 열었습니다. 창에서 보내기를 눌러 주세요.', true);
    });
    document.getElementById('inquiry-copy').addEventListener('click', function () {
      var body = collect(); if (!body) return;
      var done = function () { say('내용을 복사했습니다. ' + to + ' 로 보내 주세요.', true); };
      var fail = function () { say('복사하지 못했습니다. 내용을 직접 선택해 복사해 주세요.'); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(body).then(done, fail); else fail();
    });
  }

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
