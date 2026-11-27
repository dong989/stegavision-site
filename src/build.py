#!/usr/bin/env python3
"""스테가비전 사이트 생성기.
- 글은 pages/ 폴더의 페이지별 파일에서 고친다.
- 공통 정보(메일, 전화, 주소)는 아래 SITE 에서 한 번만 고친다.
- python3 src/build.py          → 저장소 맨 위에 실제 배포용 파일 생성 (주소: /home, /service ...)
- python3 src/build.py preview  → 미리보기용 (링크에 .html 을 붙임)
"""
import sys, pathlib, datetime, hashlib, json

ROOT = pathlib.Path(__file__).parent
OUT = ROOT.parent  # 저장소 맨 위가 실제 사이트
PREVIEW = len(sys.argv) > 1 and sys.argv[1] == "preview"
EXT = ".html" if PREVIEW else ""
# stegavision.com 을 GitHub Pages 에 연결한 뒤 True 로 바꾼다 (CNAME 파일 생성)
CUSTOM_DOMAIN_LIVE = True

SITE = {
    "domain": "https://stegavision.com",
    "name": "스테가비전",
    "email": "zowha989@gmail.com",
    "phone": "010-9936-4030",
    "address": "경상북도 경산시 대학로 280, 전기관 303-1",
    "ceo": "김유정",
    # 검색 등록 소유확인 값 (기존 아임웹 사이트에 들어 있던 값 그대로)
    "google_verify": "XK7L8C0LI_04KLY4gl_IOighH7ABKHWZkvfeISSYv18",
    "naver_verify": "a3b0773f67b0acd163d88f2594204935354821e5",  # 2026.11.23 대표 네이버 계정에서 발급 (이전 값 ac2b2785...은 타 계정 것이라 제거)
}

PAGES = [
    # 파일, 메뉴 이름, 제목, 설명
    ("home", "홈", "스테가비전 ㅣ 디지털 인증의 새로운 기준",
     "스테가비전은 AI 기반 Invisible Steganography 인증 기술로 보이지 않는 보안을 선도하는 기업입니다."),
    ("about-stegavision", "회사소개", "회사소개 | 스테가비전 - 보이지 않는 보안을 설계하다",
     "스테가비전은 AI 기반 영상보안 기술을 연구하는 전문기업으로, Invisible Steganography 기술을 통해 영상 속 데이터의 진위와 보안을 지키는 새로운 표준을 제시합니다."),
    ("service", "서비스 안내", "서비스 안내 | 스테가비전 Invisible Watermark & 정품인증 솔루션",
     "AI 워터마크, 영상 데이터 보안, 정품인증 라벨 등 스테가비전의 핵심 기술 서비스를 소개합니다. 산업·의료·콘텐츠·국방 분야에 적용 가능한 AI 보안 솔루션을 만나보세요."),
    ("contact", "문의하기", "문의하기 | 스테가비전 기술 제휴 및 파트너십 문의",
     "스테가비전의 AI 기반 영상보안 기술에 관심이 있으신가요? 기술 협력, 사업 제휴, 정품 인증 솔루션 도입 관련 문의를 환영합니다."),
]

# 뉴스 기사 페이지 (메뉴에는 나오지 않음): 파일, 제목, 설명
NEWS = [
    ("news-yunicorn-esg-2024", "영남대 창업지원단, 제2회 2024년 YUnicorn ESG창업경진대회 개최 | 스테가비전",
     "스테가비전이 제2회 2024년 YUnicorn ESG창업경진대회에서 예비창업자 트랙 대상을 받았습니다."),
    ("privacy", "개인정보처리방침 | 스테가비전", "스테가비전 홈페이지의 개인정보 처리 항목과 이용 목적 안내입니다."),
]

# 영문판: 파일, 메뉴 이름, 제목, 설명 (글은 pages/en/ 폴더)
PAGES_EN = [
    ("home", "Home", "StegaVision | A New Standard for Digital Authentication",
     "StegaVision leads invisible security with AI-based Invisible Steganography authentication technology."),
    ("about-stegavision", "About", "About | StegaVision - Designing Invisible Security",
     "StegaVision researches AI-based visual security and uses Invisible Steganography to protect the authenticity and security of data inside images and video."),
    ("service", "Service", "Service | StegaVision Invisible Watermark & Product Authentication",
     "AI watermarking, video data security and product authentication labels: the core technology services of StegaVision."),
    ("contact", "Contact", "Contact | StegaVision - Technology Partnership Inquiries",
     "Interested in StegaVision's AI-based visual security technology? We welcome inquiries about technical cooperation, partnerships and product authentication solutions."),
]
NEWS_EN = [
    ("news-yunicorn-esg-2024", "Grand Prize at the 2nd YUnicorn ESG Startup Competition | StegaVision",
     "StegaVision won the Grand Prize in the pre-founder track at the 2nd YUnicorn ESG Startup Competition 2024."),
    ("privacy", "Privacy Policy | StegaVision", "What personal information the StegaVision website handles and why."),
]
# 영문판에서만 바꿔 끼우는 그림 (src/make_en_images.py 로 만든다)
EN_IMAGES = ["business-diagram.jpg", "technology-flow.jpg", "technology-flow-m.png", "hidn-detect.png"]
T = {
    "ko": {"lang": "ko", "site": "스테가비전", "logo_alt": "스테가비전 StegaVision", "nav": "주 메뉴", "app": "앱 다운로드", "menu": "메뉴 열기",
           "company": "회사명 : 스테가비전(StegaVision)　대표자 : {ceo}", "addr": "주소 : {address}", "tel": "대표번호 : {phone}", "mail": "이메일",
           "privacy": "개인정보처리방침", "copy": "Copyright ⓒ 스테가비전 All rights reserved.", "top": "맨 위로", "zoom": "이미지 크게 보기", "close": "닫기",
           "switch": "EN", "switch_label": "English"},
    "en": {"lang": "en", "site": "StegaVision", "logo_alt": "StegaVision", "nav": "Main menu", "app": "App Download", "menu": "Open menu",
           "company": "Company : StegaVision　CEO : {ceo}", "addr": "Address : {address}", "tel": "Tel : {phone}", "mail": "Email",
           "privacy": "Privacy Policy", "copy": "Copyright ⓒ StegaVision All rights reserved.", "top": "Back to top", "zoom": "Enlarged image", "close": "Close",
           "switch": "KO", "switch_label": "한국어"},
}
SITE_EN = {"ceo": "Yujeong Kim", "phone": "+82-10-9936-4030",
           "address": "303-1, Electrical Engineering Bldg., 280 Daehak-ro, Gyeongsan-si, Gyeongsangbuk-do, Republic of Korea"}

ICON_DOWNLOAD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11"/><path d="M7 11l5 5 5-5"/><path d="M5 20h14"/></svg>'
ICON_INSTA = '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1" fill="#fff" stroke="none"/></svg>'
ICON_BLOG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M4 4h16a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-5.5L12 20.5 9.5 17H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><text x="12" y="13.5" text-anchor="middle" font-size="7" font-weight="700" font-family="Arial,sans-serif" fill="#aaa">blog</text></svg>'
ICON_ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg>'


def asset_version():
    """스타일·스크립트가 바뀌면 방문자 브라우저가 새 파일을 받도록 주소 뒤에 붙이는 값"""
    h = hashlib.md5()
    for f in ("assets/css/site.css", "assets/js/site.js"):
        h.update((OUT / f).read_bytes())
    return h.hexdigest()[:8]


def href(slug):
    return f"{slug}{EXT}"


def render(slug, menu_name, title, desc, lang="ko"):
    en = lang == "en"
    t = T[lang]
    site = dict(SITE, **SITE_EN) if en else SITE
    pages = PAGES_EN if en else PAGES
    body = (ROOT / "pages" / ("en" if en else "") / f"{slug}.html").read_text(encoding="utf-8")
    body = body.replace("<br>", "<br> ")  # 모바일에서 줄바꿈을 없앨 때 낱말이 붙지 않게
    nav = "".join(
        f'<a href="{href(s)}"{" class=\"on\" aria-current=\"page\"" if s == slug or (s == "about-stegavision" and slug.startswith("news-")) else ""}>{n}</a>'
        for s, n, _, _ in pages)
    ko_href, en_href = ("../" if en else "") + href(slug), ("" if en else "en/") + href(slug)
    nav += (f'<span class="lang"><a href="{ko_href}" lang="ko" aria-label="한국어"{"" if en else " class=\"on\" aria-current=\"true\""}>KO</a>'
            f'<a href="{en_href}" lang="en" aria-label="English"{" class=\"on\" aria-current=\"true\"" if en else ""}>EN</a></span>')
    url = f'{SITE["domain"]}/{"en/" if en else ""}{slug}'
    alt_ko, alt_en = f'{SITE["domain"]}/{slug}', f'{SITE["domain"]}/en/{slug}'
    ld = ""
    if slug == "home":
        ld = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "Organization",
            "name": "스테가비전", "alternateName": "StegaVision", "url": SITE["domain"],
            "logo": SITE["domain"] + "/assets/img/icon-196.png",
            "email": SITE["email"], "telephone": "+82-10-9936-4030",
            "founder": {"@type": "Person", "name": "김유정"},
            "address": {"@type": "PostalAddress", "streetAddress": "대학로 280, 전기관 303-1",
                        "addressLocality": "경산시", "addressRegion": "경상북도", "addressCountry": "KR"},
        }, ensure_ascii=False) + "</script>\n"
    html = f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ko" href="{alt_ko}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="x-default" href="{alt_ko}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{t['site']}">
<meta property="og:locale" content="{"en_US" if en else "ko_KR"}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE['domain']}/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="610">
<meta name="theme-color" content="#206cd4">
<!-- 검색 등록 소유확인 (구글 서치콘솔 / 네이버 서치어드바이저) -->
<meta name="google-site-verification" content="{SITE['google_verify']}">
<meta name="naver-site-verification" content="{SITE['naver_verify']}">
<link rel="icon" type="image/png" sizes="196x196" href="assets/img/icon-196.png">
<link rel="apple-touch-icon" sizes="152x152" href="assets/img/icon-152.png">
<link rel="preload" href="assets/fonts/PretendardVariable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css?v={asset_version()}">
{ld}</head>
<body>
<header class="header">
  <div class="wrap">
    <a class="logo" href="{href('home')}"><img src="assets/img/logo.png" alt="{t['logo_alt']}" width="189" height="24"></a>
    <nav class="nav" aria-label="{t['nav']}">{nav}</nav>
    <span class="btn-app" aria-disabled="true">{ICON_DOWNLOAD}{t['app']}</span>
    <button class="menu-btn" aria-label="{t['menu']}" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>
<main>
{body}
</main>
<footer class="footer">
  <div class="wrap">
    <img class="f-logo" src="assets/img/logo-footer.png" alt="{t['logo_alt']}" width="203" height="26">
    <div class="sns" aria-hidden="true"><span>{ICON_INSTA}</span><span>{ICON_BLOG}</span></div>
    <p class="info">
      <span>{t['company'].format(**site)}</span><br>
      <span>{t['addr'].format(**site)}</span><i>ㅣ</i><span>{t['tel'].format(**site)}</span><i>ㅣ</i><span>{t['mail']} : <a href="mailto:{SITE['email']}">{SITE['email']}</a></span>
    </p>
    <p class="copy"><a href="{href('privacy')}">{t['privacy']}</a> ㅣ {t['copy']}</p>
  </div>
</footer>
<button class="to-top" aria-label="{t['top']}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5"/><path d="M6 11l6-6 6 6"/></svg></button>
<div class="lightbox" role="dialog" aria-label="{t['zoom']}"><button aria-label="{t['close']}">×</button><img alt=""></div>
<script src="assets/js/site.js?v={asset_version()}"></script>
</body>
</html>
"""
    for k, v in site.items():
        html = html.replace("{{" + k + "}}", v)
    if en:  # 영문판은 en/ 폴더에 있으므로 공통 자산 경로를 한 단계 위로
        for n in EN_IMAGES:
            html = html.replace(f'assets/img/{n}', f'assets/img/en/{n}')
        html = html.replace('"assets/', '"../assets/').replace("url('assets/", "url('../assets/")
    html = html.replace("{{arrow}}", ICON_ARROW)
    for s in [x[0] for x in PAGES] + [x[0] for x in NEWS]:
        html = html.replace("{{link:" + s + "}}", href(s))
    return html


def main():
    for slug, menu, title, desc in PAGES:
        (OUT / f"{slug}.html").write_text(render(slug, menu, title, desc), encoding="utf-8")
    for slug, title, desc in NEWS:
        (OUT / f"{slug}.html").write_text(render(slug, "", title, desc), encoding="utf-8")
    # 영문판 (/en/...)
    (OUT / "en").mkdir(exist_ok=True)
    for slug, menu, title, desc in PAGES_EN:
        (OUT / "en" / f"{slug}.html").write_text(render(slug, menu, title, desc, "en"), encoding="utf-8")
    for slug, title, desc in NEWS_EN:
        (OUT / "en" / f"{slug}.html").write_text(render(slug, "", title, desc, "en"), encoding="utf-8")
    (OUT / "en" / "index.html").write_text(render(*PAGES_EN[0], "en"), encoding="utf-8")
    # 첫 화면(/)은 홈과 같은 내용
    (OUT / "index.html").write_text(render(*PAGES[0]), encoding="utf-8")
    today = datetime.date.today().isoformat()
    urls = "".join(f"<url><loc>{SITE['domain']}/{s}</loc><lastmod>{today}</lastmod></url>" for s, *_ in PAGES + NEWS) + "".join(f"<url><loc>{SITE['domain']}/en/{s}</loc><lastmod>{today}</lastmod></url>" for s, *_ in PAGES_EN + NEWS_EN)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',
        encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE['domain']}/sitemap.xml\n", encoding="utf-8")
    if CUSTOM_DOMAIN_LIVE:
        (OUT / "CNAME").write_text("stegavision.com\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUT / "404.html").write_text('<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>페이지를 찾을 수 없습니다 | 스테가비전</title><meta http-equiv="refresh" content="3;url=/home"></head><body style="font-family:sans-serif;text-align:center;padding:80px 20px"><h1>페이지를 찾을 수 없습니다</h1><p><a href="/home">스테가비전 홈으로 이동</a></p></body></html>', encoding="utf-8")
    print("built", "preview" if PREVIEW else "production", "->", OUT)


if __name__ == "__main__":
    main()
