# 스테가비전 홈페이지

stegavision.com 의 정적 사이트입니다. GitHub Pages 로 배포합니다.

## 구조
- 맨 위 폴더: 실제로 서비스되는 파일 (`index.html`, `home.html`, `about-stegavision.html`, `service.html`, `contact.html`, `assets/`)
- `src/pages/`: 페이지별 글. 글은 여기서 고칩니다.
- `src/build.py`: 공통 메뉴·하단과 합쳐 맨 위 폴더의 HTML 을 다시 만듭니다. 메일·전화·주소는 이 파일의 `SITE` 에서 한 번만 고칩니다.

## 고치는 방법
1. `src/pages/*.html` 또는 `assets/img/` 수정
2. `python3 src/build.py` 실행
3. 변경된 파일을 커밋하고 `main` 에 올리면 사이트에 반영됩니다.

## 주의
- 공개 저장소입니다. 홈페이지에 공개하는 내용만 올립니다.
