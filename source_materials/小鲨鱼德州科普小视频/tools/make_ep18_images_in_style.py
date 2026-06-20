from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EP17 = ROOT / "17_什么是被压制dominated" / "01_手绘图片"
EP16 = ROOT / "16_什么是反向隐含赔率reverse_implied_odds" / "01_手绘图片"
EP18 = ROOT / "18_什么是持续下注continuation_bet"
OUT = EP18 / "01_手绘图片"
REVIEW = EP18 / "_style_review"

FONT_BOLD = Path("C:/Windows/Fonts/NotoSansSC-VF.ttf")
FONT_REG = Path("C:/Windows/Fonts/msyh.ttc")


SCENES = [
    ("01_开场什么是Cbet", "什么是\nC-bet？", ["上期预告：持续下注", "这期：C-bet"], "intro"),
    ("02_主题持续下注continuation_bet", "持续下注", ["continuation bet", "C-bet", "第18期"], "title"),
    ("03_核心定义", "核心定义", ["翻前主动加注者", "翻牌后继续下注"], "definition"),
    ("04_继续这个故事", "继续这个故事", ["翻前：我很强", "翻后：继续讲"], "story"),
    ("05_翻前open_raise", "翻前\nopen raise", ["我主动加注", "3BB 示例"], "open"),
    ("06_别人跟注call", "别人跟注", ["call", "进入翻牌"], "call"),
    ("07_翻牌后再下注", "翻牌后\n再下注", ["这一下就是 C-bet"], "flop_bet"),
    ("08_不一定中了牌", "不一定\n中了牌", ["不是因为一定中牌"], "not_hit"),
    ("09_强范围继续讲故事", "强范围", ["继续讲故事", "不是瞎讲"], "range_story"),
    ("10_新手误会自动Cbet", "自动\nC-bet？", ["翻前加注 ≠ 必须下注"], "auto"),
    ("11_不是必须", "不是必须", ["C-bet 是选择", "不是按钮"], "not_must"),
    ("12_选择不是自动按钮", "它是选择", ["下注", "过牌", "调整计划"], "choices"),
    ("13_适合Cbet的牌面", "适合继续\n下注？", ["先看牌面"], "good_board"),
    ("14_A高K高干燥牌面", "A 高牌面", ["A 7 2", "比较干燥"], "dry"),
    ("15_加注者更像打中", "谁更像\n打中？", ["翻前加注者", "范围更匹配"], "range_match"),
    ("16_AK_AQ_AA_KK故事顺", "故事比较顺", ["AK", "AQ", "AA", "KK"], "strong_hands"),
    ("17_不舒服的牌面", "不舒服的\n牌面", ["先停一下", "别自动下注"], "uncomfortable"),
    ("18_876连牌", "8 7 6\n连牌", ["连接很紧", "更湿润"], "wet"),
    ("19_跟注者可能更容易中", "跟注者\n也容易中", ["小对子", "同花连张", "连接牌"], "caller_hits"),
    ("20_故事不自然", "我很强？", ["故事没那么自然"], "question_story"),
    ("21_看对手人数", "人数很重要", ["单挑", "多人"], "people"),
    ("22_单挑更容易成功", "单挑底池", ["C-bet 更清楚"], "heads_up"),
    ("23_多人底池风险", "多人底池", ["有人可能中牌"], "multiway"),
    ("24_人越多越小心", "人越多", ["越要小心", "别乱 C-bet"], "careful"),
    ("25_不只是诈唬", "不只是诈唬", ["价值下注", "诈唬/半诈唬"], "two_purpose"),
    ("26_有强牌拿价值", "有强牌", ["拿价值"], "value"),
    ("27_没中也可能代表范围", "没中也可以\n代表范围", ["强范围还在"], "miss_range"),
    ("28_希望对手怎么反应", "先问目的", ["想让对手跟？", "还是弃？"], "reaction"),
    ("29_价值下注目的", "价值下注", ["希望被差牌跟"], "value_goal"),
    ("30_诈唬半诈唬目的", "诈唬/\n半诈唬", ["希望对手弃牌"], "bluff_goal"),
    ("31_三个问题登场", "先问 3 个问题", ["C-bet 检查清单"], "checklist"),
    ("32_问题一牌面对范围有利吗", "问题一", ["牌面对我的范围有利吗？"], "q1"),
    ("33_问题二人数和命中", "问题二", ["人多吗？", "对手像中牌吗？"], "q2"),
    ("34_问题三下注目的", "问题三", ["拿价值？", "让对手弃牌？"], "q3"),
    ("35_小口诀", "小口诀", ["翻前我主动，翻后可继续", "牌面讲得通，才是好 C-bet"], "slogan"),
    ("36_下期预告干燥湿润牌面", "下期预告", ["干燥牌面", "湿润牌面"], "next"),
    ("37_合规结尾理性观看", "知识科普", ["娱乐假设", "不宣传赌博", "理性观看"], "end"),
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


def whitewash(im, boxes):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for box, alpha, radius in boxes:
        ld.rounded_rectangle(box, radius=radius, fill=(255, 255, 255, alpha))
    im.alpha_composite(layer)


def cloud(d, box, fill=(255, 255, 255), outline=(18, 26, 56), width=8):
    x1, y1, x2, y2 = box
    d.rounded_rectangle((x1 + 18, y1 + 45, x2 - 18, y2 - 12), radius=54, fill=fill, outline=outline, width=width)
    bumps = [
        (x1 + 90, y1 + 92, 74), (x1 + 205, y1 + 72, 88),
        (x1 + 350, y1 + 80, 86), (x2 - 220, y1 + 75, 90),
        (x2 - 95, y1 + 96, 72),
    ]
    for cx, cy, r in bumps:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=outline, width=width)
    d.arc((x1 + 135, y2 - 75, x2 - 135, y2 - 18), 185, 350, fill=(242, 190, 30), width=8)


def label(d, box, text, fill=(255, 249, 218), txt=(20, 48, 150), size=36):
    rounded(d, box, fill=fill, outline=(35, 35, 35), width=5, radius=18)
    center_text(d, box, text, font(size), txt, sw=1)


def note(d, box, text, fill=(255, 255, 255), txt=(18, 45, 150), size=38):
    rounded(d, box, fill=fill, outline=(32, 44, 70), width=6, radius=24)
    center_text(d, box, text, font(size), txt, sw=1)


def card(d, box, rank, suit="", tint=(255, 255, 255), big=True):
    rounded(d, box, fill=tint, outline=(25, 25, 25), width=6, radius=16)
    color = (205, 40, 45) if suit in {"♥", "♦"} else (15, 24, 40)
    center_text(d, box, f"{rank}\n{suit}".strip(), font(58 if big else 42), color, sw=1)


def chip(d, x, y, r=34):
    d.ellipse((x-r, y-r, x+r, y+r), fill=(220, 235, 255), outline=(20, 58, 155), width=5)
    d.ellipse((x-r*0.55, y-r*0.55, x+r*0.55, y+r*0.55), fill=(255, 255, 255), outline=(20, 58, 155), width=3)


def arrow(d, start, end, fill=(45, 108, 220), width=12):
    d.line((start, end), fill=fill, width=width)
    ex, ey = end
    sx, sy = start
    import math
    ang = math.atan2(ey - sy, ex - sx)
    pts = [(ex, ey)]
    for delta in (2.55, -2.55):
        pts.append((ex - math.cos(ang + delta) * 38, ey - math.sin(ang + delta) * 38))
    d.polygon(pts, fill=fill)


def flop(d, ranks=("A", "7", "2"), suits=("♥", "♣", "♦"), y=430, x=250):
    for rank, suit in zip(ranks, suits):
        card(d, (x, y, x + 145, y + 205), rank, suit)
        x += 175


def get_ref_paths():
    def num(p):
        m = re.match(r"(\d+)_", p.name)
        return int(m.group(1)) if m else 999

    refs = sorted(EP17.glob("*_1080x1920.png"), key=num)
    extra = sorted(EP16.glob("*_1080x1920.png"), key=num)
    if len(refs) < 36 or not extra:
        raise RuntimeError("Reference images missing. Need EP17 and EP16 finished images.")
    return refs + extra[:1]


def draw_common(im, title, idx):
    d = ImageDraw.Draw(im)
    whitewash(im, [((12, 20, 1068, 390), 252, 46), ((45, 365, 1035, 950), 235, 36)])
    rounded(d, (52, 58, 1028, 330), fill=(255, 255, 255), outline=(18, 26, 56), width=8, radius=46)
    d.arc((150, 255, 930, 330), 185, 355, fill=(242, 190, 30), width=8)
    clean = title.replace("\n", "")
    size = 91 if len(clean) <= 5 else 78 if len(clean) <= 9 else 66
    center_text(d, (110, 88, 970, 265), title, font(size), (8, 34, 145), sw=3)
    label(d, (790, 78, 970, 150), f"第18期", fill=(255, 232, 92), txt=(8, 34, 145), size=34)
    return d


def draw_kind(d, kind, lines):
    if kind == "title":
        label(d, (240, 370, 840, 475), lines[0], fill=(239, 248, 255), txt=(20, 55, 160), size=48)
        label(d, (365, 535, 715, 640), lines[1], fill=(255, 235, 105), txt=(8, 34, 145), size=58)
    elif kind in {"intro", "definition", "story", "range_story", "not_must", "choices", "uncomfortable", "question_story", "careful", "reaction", "checklist", "q3", "slogan", "next", "end", "auto"}:
        y = 405
        for line in lines:
            note(d, (150, y, 930, y + 92), line, size=38 if len(line) < 15 else 32)
            y += 122
        if kind == "auto":
            label(d, (365, 725, 715, 830), "自动按钮？", fill=(255, 232, 232), txt=(180, 48, 45), size=42)
    elif kind in {"open", "call", "flop_bet"}:
        if kind == "flop_bet":
            flop(d, ("A", "7", "2"), ("♥", "♣", "♦"), 400, 275)
            label(d, (390, 655, 690, 745), "bet / 下注", fill=(255, 235, 105), size=42)
            arrow(d, (540, 840), (540, 745))
        else:
            note(d, (220, 395, 860, 500), lines[0], size=46)
            for x in (445, 515, 585):
                chip(d, x, 625, 34)
            label(d, (380, 700, 700, 790), lines[1], fill=(255, 235, 105), size=40)
            arrow(d, (540, 840), (540, 680))
    elif kind in {"good_board", "dry"}:
        flop(d, ("A", "7", "2"), ("♥", "♣", "♦"), 405, 275)
        label(d, (260, 665, 820, 760), lines[0] if kind == "good_board" else lines[1], size=42)
        if kind == "dry":
            label(d, (390, 785, 690, 875), "牌面很分散", fill=(239, 248, 255), size=38)
    elif kind == "range_match":
        label(d, (135, 410, 480, 570), lines[0], fill=(238, 248, 255), txt=(20, 70, 160), size=42)
        label(d, (600, 455, 945, 615), "跟注者", fill=(255, 244, 230), txt=(180, 70, 55), size=42)
        d.line((210, 710, 870, 760), fill=(45, 45, 45), width=13)
        d.polygon([(280, 760), (330, 760), (305, 875)], fill=(238, 248, 255), outline=(35, 35, 35))
        note(d, (300, 610, 780, 700), lines[1], size=40)
    elif kind == "strong_hands":
        for x, txt in [(175, "AK"), (385, "AQ"), (595, "AA"), (805, "KK")]:
            label(d, (x, 405, x + 135, 500), txt, fill=(238, 248, 255), txt=(20, 70, 160), size=42)
        flop(d, ("A", "7", "2"), ("♥", "♣", "♦"), 580, 275)
        note(d, (280, 815, 800, 900), "A 高牌面故事顺", size=38)
    elif kind == "wet":
        flop(d, ("8", "7", "6"), ("♠", "♥", "♣"), 405, 275)
        arrow(d, (355, 665), (725, 665), fill=(210, 70, 55))
        label(d, (360, 720, 720, 810), lines[0], fill=(255, 244, 230), txt=(180, 62, 45), size=42)
    elif kind == "caller_hits":
        y = 395
        for line in lines:
            label(d, (180, y, 900, y + 88), line, fill=(255, 244, 230), txt=(170, 65, 50), size=40)
            y += 118
        flop(d, ("8", "7", "6"), ("♠", "♥", "♣"), 765, 300)
    elif kind in {"people", "heads_up", "multiway"}:
        label(d, (160, 405, 465, 515), lines[0], fill=(238, 248, 255), size=42)
        label(d, (620, 405, 925, 515), lines[1] if len(lines) > 1 else "对手", fill=(255, 244, 230), txt=(170, 65, 50), size=42)
        count = 2 if kind == "heads_up" else 4 if kind == "multiway" else 3
        for i in range(count):
            x = 230 + i * 175
            d.ellipse((x, 610, x + 88, 698), fill=(238, 248, 255), outline=(35, 35, 35), width=5)
        note(d, (250, 770, 830, 860), lines[0], size=40)
    elif kind == "two_purpose":
        label(d, (115, 420, 505, 595), lines[0], fill=(238, 248, 255), txt=(20, 70, 160), size=46)
        label(d, (575, 420, 965, 595), lines[1], fill=(255, 244, 230), txt=(170, 65, 50), size=42)
        note(d, (165, 700, 915, 795), "C-bet 可以有不同目的", size=38)
    elif kind in {"value", "value_goal"}:
        card(d, (335, 405, 505, 645), "A", "♥")
        card(d, (560, 405, 730, 645), "K", "♣")
        label(d, (315, 720, 765, 815), lines[0], fill=(255, 235, 105), size=42)
        arrow(d, (540, 875), (540, 815), fill=(45, 108, 220))
    elif kind in {"miss_range", "bluff_goal"}:
        card(d, (335, 405, 505, 645), "Q", "♣")
        card(d, (560, 405, 730, 645), "J", "♠")
        label(d, (300, 720, 780, 815), lines[0], fill=(255, 244, 230), txt=(170, 65, 50), size=42)
        note(d, (280, 835, 800, 925), "强范围还在", size=38)
    elif kind == "q1":
        flop(d, ("A", "7", "2"), ("♥", "♣", "♦"), 390, 180)
        flop(d, ("8", "7", "6"), ("♠", "♥", "♣"), 650, 180)
        note(d, (235, 860, 845, 940), "哪边更有利？", size=42)
    elif kind == "q2":
        label(d, (175, 420, 455, 520), lines[0], fill=(238, 248, 255), size=40)
        label(d, (625, 420, 905, 520), lines[1], fill=(255, 244, 230), txt=(170, 65, 50), size=38)
        for x in (255, 680, 765, 850):
            d.ellipse((x, 635, x + 78, 713), fill=(238, 248, 255), outline=(35, 35, 35), width=5)


def render():
    OUT.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    refs = get_ref_paths()
    for idx, (stem, title, lines, kind) in enumerate(SCENES, 1):
        im = Image.open(refs[idx - 1]).convert("RGBA")
        if im.size != (1080, 1920):
            im = im.resize((1080, 1920), Image.Resampling.LANCZOS)
        d = draw_common(im, title, idx)
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
