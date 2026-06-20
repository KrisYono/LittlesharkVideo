from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EP16 = ROOT / "16_什么是反向隐含赔率reverse_implied_odds" / "01_手绘图片"
EP17 = ROOT / "17_什么是被压制dominated"
OUT = EP17 / "01_手绘图片"
REVIEW = EP17 / "_style_review"

FONT_BOLD = Path("C:/Windows/Fonts/NotoSansSC-VF.ttf")
FONT_REG = Path("C:/Windows/Fonts/msyh.ttc")


SCENES = [
    ("01_开场为什么中了也难受", "为什么中了\n也难受？", ["上一期：中了也可能多输", "这期：被压制"], "intro"),
    ("02_主题被压制dominated", "被压制", ["dominated", "第17期"], "title"),
    ("03_不是完全没希望", "不是完全\n没希望", ["只是提醒：要看对手"], "note"),
    ("04_同一类牌但更小", "同样中牌", ["我也中了", "对手更大"], "twobox"),
    ("05_弱A例子", "弱 A 例子", ["A7 登场"], "cards_a7"),
    ("06_A7对AQ", "A7 vs AQ", ["教学例子"], "compare_a"),
    ("07_翻牌来了A", "翻牌来了 A", ["两个人都中一对 A"], "flop"),
    ("08_7比Q小", "7 比 Q 小", ["踢脚差距"], "scale"),
    ("09_踢脚kicker", "踢脚 kicker", ["A 旁边那张牌"], "kicker"),
    ("10_AQ压着A7", "AQ 压着 A7", ["同样一对 A"], "cover"),
    ("11_被压制的味道", "被压制？", ["不是没牌，是常常更小"], "note"),
    ("12_我也有A误会", "我也有 A", ["先别只看这一点"], "bubble"),
    ("13_可以开心中牌", "可以开心", ["但还要继续比较"], "note"),
    ("14_还要问踢脚", "踢脚够好吗？", ["对手也有 A 怎么办"], "magnify"),
    ("15_赢小输大", "赢小\n输大？", ["被压制最麻烦的地方"], "bags"),
    ("16_麻烦点总结", "麻烦在哪里", ["中牌", "踢脚小", "难放手"], "three"),
    ("17_不是每次都害怕", "不是每次\n都害怕", ["看情况"], "cross"),
    ("18_别只看A", "别只看 A", ["两张牌都要看"], "cards_a7"),
    ("19_不只发生在A", "不只发生在 A", ["K、Q 也会有"], "ranks"),
    ("20_K9对KQ_Q8对QJ", "类似例子", ["K9 vs KQ", "Q8 vs QJ"], "matchups"),
    ("21_顶对踢脚不同", "顶对相同", ["踢脚不同"], "top_pair"),
    ("22_平静牌面看踢脚", "牌面越平静", ["越要看踢脚"], "note"),
    ("23_小同花遇大同花", "小同花", ["也可能遇到大同花"], "flush"),
    ("24_大同花压小同花", "同类也要\n比大小", ["大同花 > 小同花"], "flush"),
    ("25_三个问题登场", "先问 3 个问题", ["不要只靠感觉"], "checklist"),
    ("26_问题一只变一对", "问题一", ["中牌后常是一对？"], "check_one"),
    ("27_问题二踢脚够好吗", "问题二", ["踢脚够好吗？"], "check_two"),
    ("28_问题三更大同类牌", "问题三", ["对手会有更大同类吗？"], "check_three"),
    ("29_不舒服就谨慎", "不舒服", ["就谨慎一点"], "note"),
    ("30_谨慎不等于一定弃牌", "谨慎 ≠ 一定弃牌", ["看整体情况"], "fork"),
    ("31_别只靠我也中了", "别只靠", ["我也中了"], "note"),
    ("32_小口诀", "小口诀", ["同样中牌，比谁更大", "同样一对，看踢脚"], "slogan"),
    ("33_不错却难受", "看起来不错", ["为什么玩起来难受？"], "note"),
    ("34_少掉中了却输更多", "开始复盘", ["少掉：明明中了却输更多"], "review"),
    ("35_下期预告持续下注", "下期预告", ["持续下注", "continuation bet"], "next"),
    ("36_合规结尾理性观看", "知识科普", ["娱乐假设", "不宣传赌博", "理性观看"], "end"),
]


def font(size, bold=True):
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REG
    return ImageFont.truetype(str(path), size)


def center_text(d, box, text, fnt, fill, stroke=(255, 255, 255), sw=0, gap=8):
    lines = text.split("\n")
    sizes = []
    for line in lines:
        bb = d.textbbox((0, 0), line, font=fnt, stroke_width=sw)
        sizes.append((bb[2] - bb[0], bb[3] - bb[1]))
    total = sum(h for _, h in sizes) + gap * (len(lines) - 1)
    y = box[1] + (box[3] - box[1] - total) / 2
    for line, (w, h) in zip(lines, sizes):
        x = box[0] + (box[2] - box[0] - w) / 2
        d.text((x, y), line, font=fnt, fill=fill, stroke_width=sw, stroke_fill=stroke)
        y += h + gap


def rounded(d, box, fill, outline=(22, 22, 22), width=7, radius=28):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def cloud(d, box, fill=(255, 255, 255), outline=(18, 26, 56), width=8):
    x1, y1, x2, y2 = box
    d.rounded_rectangle((x1 + 22, y1 + 34, x2 - 22, y2 - 8), radius=48, fill=fill, outline=outline, width=width)
    bumps = [
        (x1 + 80, y1 + 55, 78), (x1 + 190, y1 + 20, 92),
        (x1 + 330, y1 + 36, 86), (x2 - 215, y1 + 24, 96),
        (x2 - 92, y1 + 58, 74),
    ]
    for cx, cy, r in bumps:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=outline, width=width)
    d.arc((x1 + 120, y2 - 70, x2 - 120, y2 - 18), 185, 350, fill=(242, 190, 30), width=8)


def label(d, box, text, fill=(255, 249, 218), txt=(20, 48, 150), size=36):
    rounded(d, box, fill=fill, outline=(35, 35, 35), width=5, radius=18)
    center_text(d, box, text, font(size), txt, sw=1)


def card(d, box, rank, suit="", tint=(255, 255, 255), big=True):
    rounded(d, box, fill=tint, outline=(25, 25, 25), width=6, radius=18)
    color = (200, 36, 42) if suit in {"♥", "♦"} else (15, 24, 40)
    text = f"{rank}\n{suit}".strip()
    center_text(d, box, text, font(58 if big else 44), color, sw=1)


def chip(d, x, y, r=34):
    d.ellipse((x-r, y-r, x+r, y+r), fill=(220, 235, 255), outline=(20, 58, 155), width=5)
    d.ellipse((x-r*0.55, y-r*0.55, x+r*0.55, y+r*0.55), fill=(255, 255, 255), outline=(20, 58, 155), width=3)


def whitewash(im, boxes):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for box, alpha, radius in boxes:
        ld.rounded_rectangle(box, radius=radius, fill=(255, 255, 255, alpha))
    im.alpha_composite(layer)


def base_paths():
    paths = sorted(EP16.glob("*_1080x1920.png"), key=lambda p: int(re.match(r"(\d+)_", p.name).group(1)))
    if len(paths) != 36:
        raise RuntimeError(f"Expected 36 EP16 reference images, got {len(paths)}")
    return paths


def draw_common(im, title, lines):
    d = ImageDraw.Draw(im)
    whitewash(im, [((24, 28, 1056, 330), 255, 42), ((58, 330, 1022, 930), 255, 34)])
    cloud(d, (95, 55, 985, 300))
    clean_title = title.replace("\n", "")
    title_size = 90 if len(clean_title) <= 5 else 78
    if "\n" in title:
        title_size = 76 if len(clean_title) > 7 else 82
    center_text(d, (130, 92, 950, 272), title, font(title_size), (8, 34, 145), sw=3)
    return d


def draw_kind(d, kind, lines):
    if kind == "title":
        label(d, (730, 245, 965, 325), lines[1], fill=(255, 235, 105), size=40)
        label(d, (235, 350, 845, 455), lines[0], fill=(239, 248, 255), txt=(20, 55, 160), size=50)
    elif kind in {"intro", "note", "bubble", "review", "next", "cross", "fork"}:
        y = 400
        for line in lines:
            label(d, (170, y, 910, y + 96), line, size=38)
            y += 130
    elif kind == "twobox":
        label(d, (160, 425, 455, 610), lines[0], fill=(235, 247, 255), txt=(20, 73, 175), size=44)
        label(d, (625, 425, 920, 610), lines[1], fill=(255, 240, 232), txt=(188, 45, 42), size=44)
        d.line((305, 645, 305, 790), fill=(45, 126, 220), width=16)
        d.line((775, 645, 775, 790), fill=(226, 83, 64), width=22)
    elif kind in {"cards_a7", "kicker", "magnify"}:
        card(d, (330, 430, 505, 675), "A", "♠")
        card(d, (560, 430, 735, 675), "7", "♦")
        if kind in {"kicker", "magnify"}:
            d.ellipse((530, 400, 770, 705), outline=(250, 180, 30), width=14)
        label(d, (305, 735, 775, 830), lines[0], size=42)
    elif kind == "compare_a":
        card(d, (155, 425, 300, 635), "A", "♠")
        card(d, (320, 425, 465, 635), "7", "♦")
        center_text(d, (492, 480, 588, 585), "vs", font(42), (30, 30, 30))
        card(d, (615, 425, 760, 635), "A", "♥", tint=(255, 246, 229))
        card(d, (780, 425, 925, 635), "Q", "♣", tint=(255, 246, 229))
        label(d, (365, 700, 715, 790), lines[0], size=40)
    elif kind == "flop":
        card(d, (305, 410, 460, 630), "A", "♥")
        rounded(d, (480, 410, 635, 630), fill=(203, 226, 255), outline=(80, 142, 220), width=6, radius=18)
        rounded(d, (655, 410, 810, 630), fill=(203, 226, 255), outline=(80, 142, 220), width=6, radius=18)
        label(d, (245, 705, 835, 805), lines[0], size=42)
    elif kind == "scale":
        d.line((210, 610, 870, 535), fill=(45, 45, 45), width=12)
        d.polygon([(520, 565), (590, 565), (555, 760)], fill=(230, 230, 230), outline=(45, 45, 45))
        card(d, (205, 705, 350, 900), "7", "♦")
        card(d, (730, 625, 875, 820), "Q", "♣")
        label(d, (610, 850, 930, 935), lines[0], size=40)
    elif kind == "cover":
        card(d, (245, 520, 390, 720), "A", "♠")
        card(d, (405, 520, 550, 720), "7", "♦")
        card(d, (520, 430, 690, 665), "A", "♥", tint=(255, 246, 229))
        card(d, (710, 430, 880, 665), "Q", "♣", tint=(255, 246, 229))
        label(d, (315, 760, 765, 850), lines[0], size=42)
    elif kind == "bags":
        rounded(d, (170, 455, 445, 775), fill=(235, 248, 255), outline=(40, 78, 160), width=7, radius=70)
        rounded(d, (620, 410, 910, 820), fill=(255, 237, 225), outline=(175, 58, 50), width=7, radius=80)
        label(d, (210, 525, 405, 625), "小赢", size=42)
        label(d, (665, 535, 865, 635), "大输？", fill=(255, 248, 218), txt=(190, 50, 44), size=44)
        for x, y, r in [(260, 705, 30), (335, 715, 30), (715, 735, 36), (795, 730, 36), (850, 685, 36)]:
            chip(d, x, y, r)
    elif kind == "three":
        for i, line in enumerate(lines):
            label(d, (180, 400 + i * 125, 900, 500 + i * 125), line, size=44)
    elif kind == "ranks":
        for x, r in [(250, "A"), (465, "K"), (680, "Q")]:
            card(d, (x, 445, x + 155, 660), r, "♠")
        label(d, (250, 730, 830, 825), lines[0], size=42)
    elif kind == "matchups":
        label(d, (120, 400, 500, 505), lines[0], size=42)
        label(d, (580, 400, 960, 505), lines[1], size=42)
        for x, a, b in [(175, "K9", "KQ"), (635, "Q8", "QJ")]:
            center_text(d, (x, 545, x + 280, 690), f"{a}\nvs\n{b}", font(44), (20, 48, 150), sw=2)
    elif kind == "top_pair":
        card(d, (220, 430, 365, 630), "K", "♠")
        card(d, (455, 430, 600, 630), "9", "♦")
        card(d, (700, 430, 845, 630), "Q", "♣")
        label(d, (240, 710, 840, 805), lines[0], size=44)
    elif kind == "flush":
        for x, r in [(185, "5"), (340, "8"), (495, "J"), (650, "A")]:
            card(d, (x, 440, x + 130, 625), r, "♠", big=False)
        label(d, (215, 715, 865, 810), lines[0], size=42)
    elif kind in {"checklist", "check_one", "check_two", "check_three", "slogan", "end"}:
        y = 390
        for line in lines:
            label(d, (135, y, 945, y + 94), line, size=38)
            y += 120
        if kind == "check_two":
            card(d, (270, 750, 390, 915), "A", "♠", big=False)
            card(d, (410, 750, 530, 915), "7", "♦", big=False)
            card(d, (610, 750, 730, 915), "A", "♥", big=False)
            card(d, (750, 750, 870, 915), "Q", "♣", big=False)


def render():
    OUT.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    refs = base_paths()
    for idx, (stem, title, lines, kind) in enumerate(SCENES, 1):
        im = Image.open(refs[idx - 1]).convert("RGBA")
        d = draw_common(im, title, lines)
        draw_kind(d, kind, lines)
        final = im.convert("RGB")
        final.save(OUT / f"{stem}_1080x1920.png", quality=95)
        final.save(OUT / f"{stem}_原图.png", quality=95)
    make_previews()


def make_previews():
    groups = [(1, 5), (6, 10), (11, 15), (16, 20), (21, 25), (26, 30), (31, 36)]
    for start, end in groups:
        imgs = []
        for i in range(start, end + 1):
            stem = SCENES[i - 1][0]
            imgs.append(Image.open(OUT / f"{stem}_1080x1920.png"))
        tw, th, label_h = 360, 640, 80
        canvas = Image.new("RGB", (tw * len(imgs), th + label_h), (245, 240, 230))
        d = ImageDraw.Draw(canvas)
        for offset, img in enumerate(imgs):
            canvas.paste(img.resize((tw, th), Image.Resampling.LANCZOS), (offset * tw, 0))
            center_text(d, (offset * tw, th, (offset + 1) * tw, th + label_h), f"{start + offset:02d}", font(34, False), (45, 45, 45))
        canvas.save(REVIEW / f"{start:02d}-{end:02d}_preview.png", quality=95)


if __name__ == "__main__":
    render()
