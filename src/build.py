#!/usr/bin/env python3
"""스테가비전 사이트 생성기.
- 글은 pages/ 폴더의 페이지별 파일에서 고친다.
- 공통 정보(메일, 전화, 주소)는 아래 SITE 에서 한 번만 고친다.
- python3 src/build.py          → 저장소 맨 위에 실제 배포용 파일 생성 (주소: /home, /service ...)
- python3 src/build.py preview  → 미리보기용 (링크에 .html 을 붙임)
"""
import sys, pathlib, datetime

ROOT = pathlib.Path(__file__).parent
OUT = ROOT.parent  # 저장소 맨 위가 실제 사이트
PREVIEW = len(sys.argv) > 1 and sys.argv[1] == "preview"
EXT = ".html" if PREVIEW else ""
# stegavision.com 을 GitHub Pages 에 연결한 뒤 True 로 바꾼다 (CNAME 파일 생성)
CUSTOM_DOMAIN_LIVE = False

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
]

ICON_DOWNLOAD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11"/><path d="M7 11l5 5 5-5"/><path d="M5 20h14"/></svg>'
ICON_INSTA = '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1" fill="#fff" stroke="none"/></svg>'
ICON_BLOG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M4 4h16a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-5.5L12 20.5 9.5 17H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><text x="12" y="13.5" text-anchor="middle" font-size="7" font-weight="700" font-family="Arial,sans-serif" fill="#aaa">blog</text></svg>'
ICON_ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg>'


def href(slug):
    return f"{slug}{EXT}"


def render(slug, menu_name, title, desc):
    body = (ROOT / "pages" / f"{slug}.html").read_text(encoding="utf-8")
    body = body.replace("<br>", "<br> ")  # 모바일에서 줄바꿈을 없앨 때 낱말이 붙지 않게
    nav = "".join(
        f'<a href="{href(s)}"{" class=\"on\" aria-current=\"page\"" if s == slug or (s == "about-stegavision" and slug.startswith("news-")) else ""}>{n}</a>'
        for s, n, _, _ in PAGES)
    url = f'{SITE["domain"]}/{slug}'
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['name']}">
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
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<header class="header">
  <div class="wrap">
    <a class="logo" href="{href('home')}"><img src="assets/img/logo.png" alt="스테가비전 StegaVision" width="189" height="24"></a>
    <nav class="nav" aria-label="주 메뉴">{nav}</nav>
    <span class="btn-app" aria-disabled="true">{ICON_DOWNLOAD}앱 다운로드</span>
    <button class="menu-btn" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>
<main>
{body}
</main>
<footer class="footer">
  <div class="wrap">
    <img class="f-logo" src="assets/img/logo-footer.png" alt="스테가비전 StegaVision" width="203" height="26">
    <div class="sns" aria-hidden="true"><span>{ICON_INSTA}</span><span>{ICON_BLOG}</span></div>
    <p class="info">
      <span>회사명 : 스테가비전(StegaVision)　대표자 : {SITE['ceo']}</span><br>
      <span>주소 : {SITE['address']}</span><i>ㅣ</i><span>대표번호 : {SITE['phone']}</span><i>ㅣ</i><span>이메일 : <a href="mailto:{SITE['email']}">{SITE['email']}</a></span>
    </p>
    <p class="copy">개인정보처리방침 ㅣ Copyright ⓒ 스테가비전 All rights reserved.</p>
  </div>
</footer>
<div class="lightbox" role="dialog" aria-label="이미지 크게 보기"><button aria-label="닫기">×</button><img alt=""></div>
<script src="assets/js/site.js"></script>
</body>
</html>
"""
    for k, v in SITE.items():
        html = html.replace("{{" + k + "}}", v)
    html = html.replace("{{arrow}}", ICON_ARROW)
    for s in [x[0] for x in PAGES] + [x[0] for x in NEWS]:
        html = html.replace("{{link:" + s + "}}", href(s))
    return html


def main():
    for slug, menu, title, desc in PAGES:
        (OUT / f"{slug}.html").write_text(render(slug, menu, title, desc), encoding="utf-8")
    for slug, title, desc in NEWS:
        (OUT / f"{slug}.html").write_text(render(slug, "", title, desc), encoding="utf-8")
    # 첫 화면(/)은 홈과 같은 내용
    (OUT / "index.html").write_text(render(*PAGES[0]), encoding="utf-8")
    today = datetime.date.today().isoformat()
    urls = "".join(f"<url><loc>{SITE['domain']}/{s}</loc><lastmod>{today}</lastmod></url>" for s, *_ in PAGES + NEWS)
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
