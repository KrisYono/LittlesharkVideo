from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EP19 = ROOT / "19_什么是干燥牌面和湿润牌面_board_texture" / "01_手绘图片"
EP20 = ROOT / "20_Cbet尺度怎么想_cbet_sizing"
OUT = EP20 / "01_手绘图片"
REVIEW = EP20 / "_style_review"

FONT_BOLD = Path("C:/Windows/Fonts/NotoSansSC-VF.ttf")
FONT_REG = Path("C:/Windows/Fonts/msyh.ttc")

SCENES = [
    ("01_开场衔接接着", "上一期：干燥 vs 湿润", ["接着讲 C-bet 尺度"], "existing"),
    ("02_主题问题Cbet下多大", "C-bet 下多大？", ["新手常见问题"], "existing"),
    ("03_术语CbetSizing尺度", "C-bet sizing", ["持续下注尺度"], "existing"),
    ("04_不是越大越厉害", "不是越大越厉害", ["下注大小不是炫耀"], "existing"),
    ("05_我想表达什么", "我想表达什么？", ["下注像一句话", "先想目的"], "story"),
    ("06_A72干燥牌面", "干燥牌面", ["A 7 2", "连接很少"], "dry_board"),
    ("07_听牌少连接少", "听牌少", ["顺子少", "同花少", "连接少"], "few_draws"),
    ("08_小注讲清楚", "小注也能讲清楚", ["一小叠筹码", "故事线延续"], "small_bet"),
    ("09_强范围不是证明", "强范围", ["翻前强范围", "不是用筹码证明"], "range"),
    ("10_安静桌面不用喊", "安静桌面", ["说话不用喊太大声"], "quiet"),
    ("11_小注不等于随便", "小注 ≠ 随便", ["先看情况"], "caution_button"),
    ("12_范围有利吗", "范围有利吗？", ["这个牌面对我好吗？"], "check_range"),
    ("13_湿润牌面登场", "湿润牌面", ["8 7 6", "连接更多"], "wet_board"),
    ("14_听牌很多", "听牌很多", ["顺子听牌", "同花听牌", "连接牌"], "many_draws"),
    ("15_太小给舒服价格", "太小？", ["继续很舒服？"], "cheap_price"),
    ("16_价值下注更扎实", "价值下注", ["有强牌", "尺度更扎实"], "solid_value"),
    ("17_不是湿润一定大注", "不是一定大注", ["湿润 ≠ 自动大注", "看目的"], "not_auto_big"),
    ("18_牌面会变化", "牌面会变化", ["转牌 / 河牌", "哪些牌会继续？"], "weather"),
    ("19_没中希望弃牌", "希望弃牌？", ["没中牌", "想靠 C-bet 施压"], "miss_fold"),
    ("20_湿润牌面要小心", "湿润要小心", ["先踩刹车", "再想清楚"], "brake"),
    ("21_对手不想放弃", "对手可能继续", ["一对", "听顺", "听花"], "opponents_continue"),
    ("22_盲目大注风险", "盲目大注", ["故事不一定可信", "风险更大"], "risk"),
    ("23_先看目的", "先看目的", ["拿价值", "让对手弃牌"], "purpose"),
    ("24_问题一目的", "问题一", ["更差跟注？", "对手弃牌？"], "fork"),
    ("25_问题二牌面", "问题二", ["干燥", "湿润"], "dry_wet_compare"),
    ("26_问题三人数", "问题三", ["单挑？", "多人？"], "players"),
    ("27_单挑小注压力", "单挑底池", ["小注有时也有压力"], "heads_up"),
    ("28_多人更容易有关", "多人底池", ["人越多", "越可能有关"], "multiway"),
    ("29_人多要谨慎", "多人别硬讲故事", ["暂停一下"], "multi_careful"),
    ("30_不要背公式", "别背公式", ["1/3 pot", "1/2 pot", "2/3 pot"], "formulas"),
    ("31_数字不是答案", "数字不是自动答案", ["常见尺寸", "先看检查清单"], "not_answer"),
    ("32_练为什么", "练为什么", ["为什么小？", "为什么大？"], "why"),
    ("33_干燥小一点框架", "干燥 + 范围优势", ["可以考虑小一点"], "dry_scale"),
    ("34_湿润扎实一点框架", "听牌多 + 强价值", ["考虑扎实一点"], "wet_scale"),
    ("35_没目的先别按", "没目的", ["先别急着按下注按钮"], "pause"),
    ("36_小口诀", "小口诀", ["干燥小声讲，湿润想清楚", "下注看目的，别把尺寸当公式"], "slogan"),
    ("37_下期预告半诈唬", "下期预告", ["半诈唬", "semi-bluff"], "next"),
    ("38_合规结尾理性观看", "知识科普", ["娱乐假设", "不宣传赌博", "理性观看"], "end"),
]

EXISTING_CHOICES = {
    1: "01_开场衔接接着_v3_1080x1920.png",
    2: "02_主题问题Cbet下多大_v2_1080x1920.png",
    3: "03_术语CbetSizing尺度_v2_1080x1920.png",
    4: "04_不是越大越厉害_v2_1080x1920.png",
}


def font(size, bold=True):
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REG
    return ImageFont.truetype(str(path), size)


def center_text(d, box, text, fnt, fill, stroke=(255, 255, 255), sw=0, gap=8):
    lines = text.split("\n")
    sizes = [d.textbbox((0, 0), line, font=fnt, stroke_width=sw) for line in lines]
    heights = [bb[3] - bb[1] for bb in sizes]
    total_h = sum(heights) + gap * (len(lines) - 1)
    y = box[1] + (box[3] - box[1] - total_h) / 2
    for line, bb in zip(lines, sizes):
        w = bb[2] - bb[0]
        h = bb[3] - bb[1]
        x = box[0] + (box[2] - box[0] - w) / 2
        d.text((x, y), line, font=fnt, fill=fill, stroke_width=sw, stroke_fill=stroke)
        y += h + gap


def rounded(d, box, fill, outline=(30, 30, 30), width=6, radius=26):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def label(d, box, text, fill=(255, 250, 222), txt=(15, 45, 150), size=38):
    rounded(d, box, fill=fill, outline=(30, 38, 60), width=5, radius=20)
    center_text(d, box, text, font(size), txt, sw=1)


def note(d, box, text, fill=(255, 255, 255), size=36):
    label(d, box, text, fill=fill, txt=(15, 45, 150), size=size)


def whitewash(im):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for box, alpha, radius in [
        ((18, 25, 1062, 360), 250, 46),
        ((42, 350, 1038, 980), 238, 36),
        ((70, 1035, 1010, 1510), 210, 34),
    ]:
        d.rounded_rectangle(box, radius=radius, fill=(255, 255, 255, alpha))
    im.alpha_composite(layer)


def draw_common(im, title):
    d = ImageDraw.Draw(im)
    whitewash(im)
    rounded(d, (70, 64, 1010, 310), fill=(255, 255, 255), outline=(18, 28, 70), width=8, radius=48)
    d.arc((180, 235, 900, 315), 185, 355, fill=(242, 190, 30), width=8)
    clean = title.replace("\n", "")
    size = 78 if len(clean) <= 8 else 66 if len(clean) <= 12 else 56
    center_text(d, (115, 92, 965, 266), title, font(size), (8, 34, 145), sw=3)
    label(d, (805, 82, 965, 145), "第20期", fill=(255, 232, 92), size=30)
    return d


def card(d, box, rank, suit="", tint=(255, 255, 255), big=True):
    rounded(d, box, fill=tint, outline=(25, 25, 25), width=6, radius=16)
    color = (205, 40, 45) if suit in {"♥", "♦"} else (15, 24, 40)
    center_text(d, box, f"{rank}\n{suit}".strip(), font(58 if big else 42), color, sw=1)


def chip(d, x, y, r=34, fill=(220, 235, 255)):
    d.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline=(20, 58, 155), width=5)
    d.ellipse((x - r * 0.55, y - r * 0.55, x + r * 0.55, y + r * 0.55), fill=(255, 255, 255), outline=(20, 58, 155), width=3)


def arrow(d, start, end, fill=(45, 108, 220), width=12):
    import math

    d.line((start, end), fill=fill, width=width)
    ex, ey = end
    sx, sy = start
    ang = math.atan2(ey - sy, ex - sx)
    pts = [(ex, ey)]
    for delta in (2.55, -2.55):
        pts.append((ex - math.cos(ang + delta) * 38, ey - math.sin(ang + delta) * 38))
    d.polygon(pts, fill=fill)


def board(d, ranks=("A", "7", "2"), suits=("♥", "♣", "♦"), x=260, y=430, gap=175):
    for rank, suit in zip(ranks, suits):
        card(d, (x, y, x + 145, y + 205), rank, suit)
        x += gap


def meter(d, box, value, color=(45, 108, 220), label_text="尺度"):
    x1, y1, x2, y2 = box
    rounded(d, box, fill=(245, 250, 255), outline=(30, 38, 60), width=5, radius=22)
    d.line((x1 + 52, (y1 + y2) // 2, x2 - 52, (y1 + y2) // 2), fill=(40, 50, 80), width=10)
    knob_x = int((x1 + 70) + value * (x2 - x1 - 140))
    d.ellipse((knob_x - 34, y1 + 24, knob_x + 34, y2 - 24), fill=color, outline=(25, 25, 25), width=4)
    center_text(d, (x1, y2 - 66, x2, y2 - 8), label_text, font(28), (15, 45, 150))


def draw_kind(d, kind, lines):
    if kind == "story":
        rounded(d, (220, 430, 860, 760), fill=(255, 249, 220), outline=(90, 70, 35), width=7, radius=32)
        d.line((540, 430, 540, 760), fill=(180, 150, 95), width=5)
        arrow(d, (540, 800), (735, 635))
        note(d, (260, 830, 820, 925), lines[0], size=40)
    elif kind in {"dry_board", "check_range", "dry_scale"}:
        board(d, ("A", "7", "2"), ("♥", "♣", "♦"), 275, 420)
        if kind == "dry_scale":
            meter(d, (210, 720, 870, 875), 0.28, label_text=lines[0])
        else:
            note(d, (250, 700, 830, 790), lines[-1], size=40)
            if kind == "check_range":
                label(d, (240, 835, 840, 930), "对我的范围有利吗？", fill=(239, 248, 255), size=36)
    elif kind == "few_draws":
        board(d, ("A", "7", "2"), ("♥", "♣", "♦"), 270, 395)
        for x, text in [(170, "顺子少"), (430, "同花少"), (690, "连接少")]:
            label(d, (x, 710, x + 220, 805), text, fill=(239, 248, 255), size=36)
        d.line((345, 650, 770, 650), fill=(160, 180, 215), width=4)
    elif kind == "small_bet":
        board(d, ("A", "7", "2"), ("♥", "♣", "♦"), 250, 400)
        for i, x in enumerate((430, 505, 580)):
            chip(d, x, 735 - i * 8, 32)
        arrow(d, (300, 850), (780, 850))
        note(d, (260, 895, 820, 980), lines[0], size=38)
    elif kind == "range":
        label(d, (150, 420, 520, 570), lines[0], fill=(239, 248, 255), size=42)
        for x in (625, 700, 775):
            chip(d, x, 505, 34)
        note(d, (180, 720, 900, 820), lines[1], size=36)
    elif kind == "quiet":
        label(d, (165, 410, 915, 525), "桌面很安静", fill=(239, 248, 255), size=44)
        board(d, ("A", "7", "2"), ("♥", "♣", "♦"), 300, 590)
        note(d, (225, 835, 855, 925), lines[0], size=38)
    elif kind == "caution_button":
        label(d, (250, 430, 830, 545), "小注按钮", fill=(255, 236, 190), size=48)
        d.ellipse((430, 620, 650, 840), fill=(255, 232, 92), outline=(40, 40, 40), width=8)
        center_text(d, (430, 620, 650, 840), "先看\n情况", font(44), (8, 34, 145), sw=2)
    elif kind in {"wet_board", "wet_scale"}:
        board(d, ("8", "7", "6"), ("♠", "♥", "♠"), 275, 420)
        for x in (340, 520, 700):
            d.arc((x - 70, 625, x + 70, 760), 20, 160, fill=(50, 145, 220), width=8)
        if kind == "wet_scale":
            meter(d, (210, 720, 870, 875), 0.68, color=(220, 92, 70), label_text=lines[0])
        else:
            note(d, (260, 780, 820, 875), lines[1], size=40)
    elif kind == "many_draws":
        board(d, ("8", "7", "6"), ("♠", "♥", "♠"), 275, 390)
        for x, text in [(125, lines[0]), (390, lines[1]), (655, lines[2])]:
            label(d, (x, 710, x + 300, 805), text, fill=(255, 244, 230), txt=(170, 65, 50), size=34)
    elif kind == "cheap_price":
        chip(d, 385, 560, 28)
        label(d, (505, 485, 850, 595), lines[0], fill=(255, 244, 230), txt=(170, 65, 50), size=38)
        board(d, ("8", "7", "6"), ("♠", "♥", "♠"), 250, 685)
    elif kind == "solid_value":
        card(d, (300, 410, 455, 625), "A", "♥")
        card(d, (475, 410, 630, 625), "A", "♣")
        for x in (665, 735, 805):
            chip(d, x, 580, 34)
            chip(d, x, 525, 34)
        meter(d, (210, 735, 870, 890), 0.63, color=(220, 92, 70), label_text=lines[1])
    elif kind == "not_auto_big":
        label(d, (170, 440, 910, 560), lines[0], fill=(255, 232, 232), txt=(175, 45, 45), size=42)
        d.line((210, 455, 870, 545), fill=(190, 45, 45), width=12)
        note(d, (320, 705, 760, 800), lines[1], size=42)
    elif kind == "weather":
        board(d, ("8", "7", "6"), ("♠", "♥", "♠"), 225, 410)
        card(d, (760, 455, 900, 645), "?", "", tint=(239, 248, 255), big=False)
        card(d, (810, 690, 950, 880), "?", "", tint=(239, 248, 255), big=False)
        note(d, (175, 790, 730, 885), lines[1], size=36)
    elif kind == "miss_fold":
        card(d, (325, 430, 480, 635), "Q", "♣")
        card(d, (520, 430, 675, 635), "J", "♦")
        board(d, ("8", "7", "6"), ("♠", "♥", "♠"), 230, 715)
        arrow(d, (760, 550), (900, 480), fill=(220, 92, 70))
        label(d, (705, 600, 970, 700), lines[1], fill=(255, 244, 230), txt=(170, 65, 50), size=32)
    elif kind == "brake":
        board(d, ("8", "7", "6"), ("♠", "♥", "♠"), 275, 420)
        d.octagon = None
        d.rounded_rectangle((370, 720, 710, 840), radius=24, fill=(255, 232, 92), outline=(30, 30, 30), width=6)
        center_text(d, (370, 720, 710, 840), "先想想", font(48), (8, 34, 145), sw=2)
    elif kind == "opponents_continue":
        board(d, ("8", "7", "6"), ("♠", "♥", "♠"), 275, 400)
        for x, text in [(160, "一对"), (410, "听顺"), (660, "听花")]:
            d.ellipse((x, 720, x + 210, 890), fill=(239, 248, 255), outline=(35, 35, 35), width=5)
            center_text(d, (x, 720, x + 210, 890), text, font(40), (15, 45, 150), sw=1)
    elif kind == "risk":
        arrow(d, (210, 570), (850, 570), fill=(220, 92, 70), width=28)
        d.line((250, 740, 830, 865), fill=(90, 90, 90), width=12)
        d.line((250, 865, 830, 740), fill=(90, 90, 90), width=12)
        note(d, (220, 900, 860, 985), lines[0], size=34)
    elif kind in {"purpose", "fork"}:
        label(d, (130, 470, 500, 610), lines[0], fill=(239, 248, 255), size=42)
        label(d, (580, 470, 950, 610), lines[1], fill=(255, 244, 230), txt=(170, 65, 50), size=42)
        arrow(d, (540, 715), (330, 615))
        arrow(d, (540, 715), (760, 615), fill=(220, 92, 70))
    elif kind == "dry_wet_compare":
        board(d, ("A", "7", "2"), ("♥", "♣", "♦"), 95, 430, gap=125)
        board(d, ("8", "7", "6"), ("♠", "♥", "♠"), 585, 430, gap=125)
        label(d, (145, 720, 455, 810), lines[0], fill=(239, 248, 255), size=42)
        label(d, (635, 720, 945, 810), lines[1], fill=(255, 244, 230), txt=(170, 65, 50), size=42)
    elif kind in {"players", "heads_up", "multiway"}:
        count = 2 if kind == "heads_up" else 4 if kind == "multiway" else 3
        d.ellipse((255, 470, 825, 795), fill=(52, 150, 95), outline=(30, 30, 30), width=8)
        for i in range(count):
            x = 250 + i * 155
            d.ellipse((x, 850 if i % 2 else 390, x + 90, 940 if i % 2 else 480), fill=(239, 248, 255), outline=(35, 35, 35), width=5)
        note(d, (230, 980, 850, 1065), lines[-1], size=36)
    elif kind == "multi_careful":
        label(d, (185, 430, 895, 555), lines[0], fill=(255, 244, 230), txt=(170, 65, 50), size=42)
        d.ellipse((450, 650, 630, 830), fill=(255, 232, 92), outline=(30, 30, 30), width=8)
        center_text(d, (450, 650, 630, 830), "暂停", font(48), (8, 34, 145), sw=2)
    elif kind == "formulas":
        for i, text in enumerate(lines):
            label(d, (185, 410 + i * 140, 895, 510 + i * 140), text, fill=(255, 250, 210), size=44)
        note(d, (250, 865, 830, 955), "不是背完就会", size=38)
    elif kind == "not_answer":
        label(d, (195, 430, 885, 545), lines[0], fill=(255, 250, 210), size=44)
        note(d, (215, 690, 865, 790), lines[1], size=40)
        for y in (830, 900, 970):
            d.line((300, y, 780, y), fill=(45, 108, 220), width=8)
    elif kind == "why":
        d.ellipse((170, 430, 500, 760), outline=(45, 108, 220), width=14)
        d.line((455, 715, 610, 870), fill=(45, 108, 220), width=18)
        label(d, (575, 420, 910, 530), lines[0], fill=(239, 248, 255), size=40)
        label(d, (575, 610, 910, 720), lines[1], fill=(255, 244, 230), txt=(170, 65, 50), size=40)
    elif kind == "pause":
        d.ellipse((390, 455, 690, 755), fill=(255, 232, 92), outline=(30, 30, 30), width=9)
        center_text(d, (390, 455, 690, 755), "先别按", font(54), (8, 34, 145), sw=2)
        note(d, (220, 835, 860, 925), lines[0], size=38)
    elif kind in {"slogan", "next", "end"}:
        y = 410
        for line in lines:
            note(d, (120, y, 960, y + 105), line, fill=(255, 255, 255), size=34 if len(line) > 15 else 42)
            y += 135
        if kind == "next":
            board(d, ("?", "?", "?"), ("", "", ""), 295, 765)
        if kind == "end":
            label(d, (250, 900, 830, 995), "理性观看", fill=(255, 232, 92), size=42)


def ref_paths():
    paths = sorted(
        EP19.glob("*_1080x1920.png"),
        key=lambda p: int(re.match(r"(\d+)_", p.name).group(1)),
    )
    if len(paths) < 38:
        raise RuntimeError(f"Need 38 EP19 reference images, got {len(paths)}")
    return paths


def scene_image_path(idx, stem):
    if idx in EXISTING_CHOICES:
        path = OUT / EXISTING_CHOICES[idx]
        if path.exists():
            return path
    return OUT / f"{stem}_1080x1920.png"


def render():
    OUT.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    refs = ref_paths()
    for idx, (stem, title, lines, kind) in enumerate(SCENES, 1):
        if kind == "existing":
            continue
        im = Image.open(refs[idx - 1]).convert("RGBA")
        if im.size != (1080, 1920):
            im = im.resize((1080, 1920), Image.Resampling.LANCZOS)
        d = draw_common(im, title)
        draw_kind(d, kind, lines)
        final = im.convert("RGB")
        final.save(OUT / f"{stem}_1080x1920.png", quality=95)
        final.save(OUT / f"{stem}_原图.png", quality=95)
    make_previews()


def make_previews():
    for start in range(1, len(SCENES) + 1, 5):
        end = min(start + 4, len(SCENES))
        imgs = []
        for i in range(start, end + 1):
            stem = SCENES[i - 1][0]
            imgs.append(Image.open(scene_image_path(i, stem)).convert("RGB"))
        tw, th, label_h = 360, 640, 80
        canvas = Image.new("RGB", (tw * len(imgs), th + label_h), (245, 240, 230))
        d = ImageDraw.Draw(canvas)
        for offset, img in enumerate(imgs):
            canvas.paste(img.resize((tw, th), Image.Resampling.LANCZOS), (offset * tw, 0))
            center_text(d, (offset * tw, th, (offset + 1) * tw, th + label_h), f"{start + offset:02d}", font(34, False), (45, 45, 45))
        canvas.save(REVIEW / f"{start:02d}-{end:02d}_preview.png", quality=95)


if __name__ == "__main__":
    render()
