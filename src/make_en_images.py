#!/usr/bin/env python3
"""영문판용 그림 만들기: 그림 속 한글 라벨을 지우고 같은 자리에 영문을 넣는다.
국문 그림을 바꾸면 이 스크립트를 다시 돌린다:  python3 src/make_en_images.py"""
import pathlib, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
ROOT = pathlib.Path(__file__).parent.parent
IMG = ROOT / "assets/img"; OUT = IMG / "en"; OUT.mkdir(exist_ok=True)
FONT = str(ROOT / "assets/fonts/PretendardVariable.woff2")

def font(size, weight):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_name(weight); return f

def relabel(name, items):
    im = Image.open(IMG / name).convert("RGB"); a = np.array(im)
    todo = []
    for (x0, y0, x1, y1), text, mode, weight, align, maxw in items:
        box = a[y0:y1, x0:x1].astype(int); lum = box.mean(axis=2)
        if mode == "dark":
            m = lum < 110
        else:
            edge = np.concatenate([box[0], box[-1], box[:, 0], box[:, -1]]); bg = np.median(edge, axis=0)
            m = np.abs(box - bg).max(axis=2) > mode
        ys, xs = np.where(m)
        if not len(xs): print("  글자를 못 찾음:", name, text); continue
        tx0, tx1, ty0, ty1 = xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0
        color = tuple(int(v) for v in np.median(box[m][lum[m] <= np.percentile(lum[m], 35)], axis=0))
        mask = np.zeros(a.shape[:2], np.uint8); mask[y0:y1, x0:x1] = m.astype(np.uint8) * 255
        mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=1)
        a = cv2.inpaint(a.astype(np.uint8), mask, 4, cv2.INPAINT_TELEA)
        todo.append((tx0, ty0, tx1, ty1, text, color, weight, align, maxw))
    im = Image.fromarray(a); d = ImageDraw.Draw(im)
    for tx0, ty0, tx1, ty1, text, color, weight, align, maxw in todo:
        h = ty1 - ty0 + 1; size = max(9, round(h * 1.02))
        while True:
            f = font(size, weight); l, t, r, b = d.textbbox((0, 0), text, font=f)
            if r - l <= (maxw or (tx1 - tx0 + 1) * 1.15) or size <= 9: break
            size -= 1
        cy = (ty0 + ty1) / 2; x = tx0 - l if align == "left" else (tx0 + tx1) / 2 - (l + r) / 2
        d.text((x, cy - (t + b) / 2), text, font=f, fill=color)
    out = OUT / name
    im.save(out, quality=93) if name.endswith(".jpg") else im.save(out, optimize=True)
    print("만듦:", out.relative_to(ROOT))

G, B = 18, 30   # 배경과의 차이 기준 (연한 글자 / 진한 글자)
relabel("business-diagram.jpg", [
    ((505, 528, 780, 585), "Conventional watermark", B, b"SemiBold", "center", 270),
    ((1120, 550, 1505, 610), "Invisible watermark", B, b"Bold", "center", 370),
])
relabel("technology-flow.jpg", [
    ((215, 402, 305, 452), "Original", B, b"Medium", "center", 150),
    ((545, 402, 665, 452), "Data", B, b"Medium", "center", 150),
    ((755, 225, 900, 278), "AI Encoder", "dark", b"Bold", "center", 140),
    ((1222, 228, 1362, 277), "AI Decoder", "dark", b"Bold", "center", 140),
    ((1610, 98, 1768, 143), "Image Info", B, b"Bold", "center", 150),
    ((1600, 168, 1675, 191), "Buyer ID", G, b"Regular", "left", 120),
    ((1600, 250, 1700, 272), "Product ID", G, b"Regular", "left", 120),
    ((1600, 332, 1675, 355), "Issue date", G, b"Regular", "left", 120),
    ((1570, 424, 1810, 480), "Detected data", B, b"Bold", "center", 250),
])
relabel("technology-flow-m.png", [
    ((165, 365, 265, 420), "Original", B, b"Medium", "center", 150),
    ((520, 365, 655, 420), "Data", B, b"Medium", "center", 150),
    ((310, 520, 480, 580), "AI Encoder", "dark", b"Bold", "center", 150),
    ((315, 1215, 485, 1268), "AI Decoder", "dark", b"Bold", "center", 150),
    ((430, 1438, 592, 1480), "Image Info", B, b"Bold", "center", 160),
    ((413, 1511, 490, 1535), "Buyer ID", G, b"Regular", "left", 120),
    ((413, 1597, 512, 1621), "Product ID", G, b"Regular", "left", 120),
    ((413, 1688, 490, 1712), "Issue date", G, b"Regular", "left", 120),
    ((380, 1785, 645, 1850), "Detected data", B, b"Bold", "center", 270),
])
relabel("hidn-detect.png", [
    ((622, 72, 735, 102), "Image Info", B, b"Bold", "center", 112),
    ((617, 112, 675, 130), "Buyer ID", G, b"Regular", "left", 90),
    ((617, 169, 690, 187), "Product ID", G, b"Regular", "left", 90),
    ((617, 226, 675, 244), "Issue date", G, b"Regular", "left", 90),
])
