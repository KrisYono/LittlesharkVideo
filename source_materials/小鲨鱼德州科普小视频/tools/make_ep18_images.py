from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / "18_什么是持续下注continuation_bet"
OUT = EP / "01_手绘图片"
REVIEW = EP / "_style_review"

FONT_BOLD = Path("C:/Windows/Fonts/NotoSansSC-VF.ttf")
FONT_REG = Path("C:/Windows/Fonts/msyh.ttc")

W, H = 1080, 1920


def font(size, bold=True):
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REG
    return ImageFont.truetype(str(path), size)


def rounded(d, box, fill, outline=(35, 35, 35), width=7, radius=28):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def center_text(d, box, text, fnt, fill=(30, 30, 30), stroke=(255, 255, 255), sw=0, gap=8):
    lines = text.split("\n")
    sizes = []
    for line in lines:
        bb = d.textbbox((0, 0), line, font=fnt, stroke_width=sw)
        sizes.append((bb[2] - bb[0], bb[3] - bb[1]))
    total_h = sum(h for _, h in sizes) + gap * (len(lines) - 1)
    y = box[1] + (box[3] - box[1] - total_h) / 2
    for line, (tw, th) in zip(lines, sizes):
        x = box[0] + (box[2] - box[0] - tw) / 2
        d.text((x, y), line, font=fnt, fill=fill, stroke_fill=stroke, stroke_width=sw)
        y += th + gap


def paper_texture(im, seed):
    random.seed(seed)
    px = im.load()
    for _ in range(3600):
        x = random.randrange(W)
        y = random.randrange(H)
        r, g, b = px[x, y][:3]
        delta = random.choice([-4, -3, 3, 4])
        px[x, y] = (max(0, min(255, r + delta)), max(0, min(255, g + delta)), max(0, min(255, b + delta)))


def star(d, x, y, r=18, fill=(255, 218, 88)):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        ang = math.pi / 2 + i * math.pi / 5
        pts.append((x + math.cos(ang) * rr, y - math.sin(ang) * rr))
    d.polygon(pts, fill=fill, outline=(60, 60, 60))


def chip(d, x, y, r=34, fill=(207, 229, 255)):
    d.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline=(38, 70, 125), width=5)
    d.ellipse((x - r * 0.58, y - r * 0.58, x + r * 0.58, y + r * 0.58), fill=(255, 255, 255), outline=(38, 70, 125), width=3)
    d.arc((x - r * 0.35, y - r * 0.2, x + r * 0.35, y + r * 0.4), 200, 340, fill=(38, 70, 125), width=3)


def card_back(im, x, y, angle=0, scale=1.0):
    w, h = int(130 * scale), int(180 * scale)
    card = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((10, 10, w + 10, h + 10), radius=int(16 * scale), fill=(207, 228, 255), outline=(90, 145, 222), width=max(3, int(5 * scale)))
    d.ellipse((w * 0.36, h * 0.38, w * 0.64 + 10, h * 0.62 + 10), fill=(255, 255, 255), outline=(90, 145, 222), width=3)
    d.arc((w * 0.39, h * 0.44, w * 0.61 + 10, h * 0.68 + 10), 200, 340, fill=(90, 145, 222), width=3)
    rot = card.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    im.paste(rot, (int(x), int(y)), rot)


def base(seed=1):
    im = Image.new("RGB", (W, H), (255, 252, 244))
    d = ImageDraw.Draw(im)
    paper_texture(im, seed)
    for x, y, a in [(80, 1545, -12), (860, 1470, 11), (815, 1665, -8), (70, 1700, 9)]:
        card_back(im, x, y, angle=a, scale=0.85)
    for x, y in [(170, 1585), (245, 1625), (755, 1565), (835, 1615), (900, 1710)]:
        chip(d, x, y, 38)
    for x, y in [(125, 260), (945, 330), (175, 1030), (918, 980)]:
        star(d, x, y)
    return im


def card(d, box, rank, suit="", fill=(255, 255, 255), big=False):
    rounded(d, box, fill=fill, outline=(30, 30, 30), width=6, radius=22)
    x1, y1, x2, y2 = box
    color = (205, 50, 55) if suit in ["♥", "♦"] else (25, 25, 35)
    center_text(d, (x1 + 8, y1 + 12, x2 - 8, y2 - 12), f"{rank}\n{suit}".strip(), font(58 if big else 44), color)


def shark(d, x, y, s=1.0, pose="point"):
    body = (190, 225, 255)
    outline = (32, 45, 65)
    d.ellipse((x, y, x + 190 * s, y + 150 * s), fill=body, outline=outline, width=int(6 * s))
    d.polygon([(x + 70 * s, y + 8 * s), (x + 106 * s, y - 48 * s), (x + 135 * s, y + 18 * s)], fill=body, outline=outline)
    d.ellipse((x + 56 * s, y + 52 * s, x + 76 * s, y + 72 * s), fill=(25, 25, 25))
    d.ellipse((x + 122 * s, y + 52 * s, x + 142 * s, y + 72 * s), fill=(25, 25, 25))
    d.arc((x + 68 * s, y + 70 * s, x + 132 * s, y + 118 * s), 15, 165, fill=outline, width=int(5 * s))
    d.ellipse((x + 38 * s, y + 82 * s, x + 66 * s, y + 103 * s), fill=(255, 170, 178))
    d.ellipse((x + 134 * s, y + 82 * s, x + 162 * s, y + 103 * s), fill=(255, 170, 178))
    if pose == "wave":
        d.line((x + 32 * s, y + 92 * s, x - 35 * s, y + 50 * s), fill=outline, width=int(7 * s))
        d.line((x + 158 * s, y + 92 * s, x + 225 * s, y + 50 * s), fill=outline, width=int(7 * s))
    else:
        d.line((x + 168 * s, y + 92 * s, x + 245 * s, y + 55 * s), fill=outline, width=int(7 * s))


def girl(d, x, y, s=1.0, note=False):
    outline = (35, 35, 35)
    d.ellipse((x + 42 * s, y, x + 168 * s, y + 130 * s), fill=(38, 34, 36), outline=outline, width=int(5 * s))
    d.ellipse((x + 55 * s, y + 30 * s, x + 155 * s, y + 142 * s), fill=(255, 220, 205), outline=outline, width=int(5 * s))
    d.pieslice((x + 50 * s, y - 22 * s, x + 160 * s, y + 70 * s), 180, 360, fill=(188, 224, 255), outline=outline, width=int(5 * s))
    d.ellipse((x + 80 * s, y + 78 * s, x + 94 * s, y + 94 * s), fill=(20, 20, 25))
    d.ellipse((x + 120 * s, y + 78 * s, x + 134 * s, y + 94 * s), fill=(20, 20, 25))
    d.arc((x + 86 * s, y + 93 * s, x + 132 * s, y + 122 * s), 20, 160, fill=outline, width=int(4 * s))
    d.ellipse((x + 63 * s, y + 98 * s, x + 84 * s, y + 116 * s), fill=(255, 160, 170))
    d.ellipse((x + 132 * s, y + 98 * s, x + 153 * s, y + 116 * s), fill=(255, 160, 170))
    rounded(d, (x + 50 * s, y + 142 * s, x + 162 * s, y + 270 * s), fill=(230, 238, 255), outline=outline, width=int(5 * s), radius=int(18 * s))
    if note:
        rounded(d, (x + 150 * s, y + 170 * s, x + 250 * s, y + 235 * s), fill=(255, 250, 210), outline=outline, width=int(4 * s), radius=int(12 * s))


def table(d):
    rounded(d, (90, 1035, 990, 1370), fill=(55, 132, 91), outline=(45, 36, 30), width=10, radius=120)
    d.arc((115, 1075, 965, 1340), 0, 180, fill=(88, 165, 120), width=5)


def header(d, text, sub=None):
    rounded(d, (75, 70, 1005, 255), fill=(238, 248, 255), outline=(38, 60, 92), width=7, radius=34)
    size = 58 if len(text.replace("\n", "")) <= 9 else 48
    center_text(d, (95, 82, 985, 182), text, font(size), (19, 70, 160), sw=2)
    if sub:
        center_text(d, (95, 175, 985, 242), sub, font(34, False), (55, 90, 145))


def label(d, box, text, color=(255, 248, 210), txt=(35, 35, 35), size=34):
    rounded(d, box, fill=color, outline=(35, 35, 35), width=5, radius=22)
    center_text(d, box, text, font(size), txt)


def board(d, title, lines):
    rounded(d, (100, 300, 980, 860), fill=(43, 116, 82), outline=(47, 36, 28), width=9, radius=30)
    center_text(d, (130, 325, 950, 420), title, font(46), (255, 249, 210), (20, 20, 20), 2)
    y = 465
    for line in lines:
        rounded(d, (155, y, 925, y + 82), fill=(250, 255, 250), outline=(35, 35, 35), width=4, radius=20)
        center_text(d, (170, y + 5, 910, y + 77), line, font(34), (35, 65, 55))
        y += 108


def arrow(d, start, end, fill=(48, 105, 205), width=12):
    d.line((start, end), fill=fill, width=width)
    ex, ey = end
    sx, sy = start
    ang = math.atan2(ey - sy, ex - sx)
    pts = []
    for a in [ang, ang + 2.55, ang - 2.55]:
        pts.append((ex - math.cos(a) * 38, ey - math.sin(a) * 38) if a != ang else (ex, ey))
    d.polygon(pts, fill=fill)


def flop(d, ranks=("A", "7", "2"), suits=("♥", "♣", "♦"), y=500):
    x = 280
    for rank, suit in zip(ranks, suits):
        card(d, (x, y, x + 145, y + 205), rank, suit, big=True)
        x += 175


SCENES = [
    ("01_开场什么是Cbet", "什么是 C-bet？", ["上期预告：持续下注"], "intro"),
    ("02_主题持续下注continuation_bet", "持续下注", ["continuation bet", "C-bet"], "title"),
    ("03_核心定义", "核心定义", ["翻前主动加注者", "翻牌后继续下注"], "definition"),
    ("04_继续这个故事", "继续这个故事", ["翻前：我很强", "翻后：继续讲"], "story"),
    ("05_翻前open_raise", "翻前 open raise", ["我主动加注"], "open"),
    ("06_别人跟注call", "别人跟注", ["call"], "call"),
    ("07_翻牌后再下注", "翻牌后再下注", ["这一下就是 C-bet"], "flop_bet"),
    ("08_不一定中了牌", "不一定中了牌", ["不是一定中牌"], "not_hit"),
    ("09_强范围继续讲故事", "强范围", ["继续讲故事"], "range_story"),
    ("10_新手误会自动Cbet", "自动 C-bet？", ["新手常误会"], "auto"),
    ("11_不是必须", "不是必须", ["看情况"], "not_must"),
    ("12_选择不是自动按钮", "它是选择", ["下注", "过牌", "调整计划"], "choices"),
    ("13_适合Cbet的牌面", "适合继续下注？", ["先看牌面"], "good_board"),
    ("14_A高K高干燥牌面", "A 高干燥牌面", ["A 7 2"], "dry"),
    ("15_加注者更像打中", "加注者更像打中", ["范围更匹配"], "scale_range"),
    ("16_AK_AQ_AA_KK故事顺", "故事比较顺", ["AK", "AQ", "AA", "KK"], "strong_hands"),
    ("17_不舒服的牌面", "不舒服的牌面", ["先停一下"], "uncomfortable"),
    ("18_876连牌", "8 7 6 连牌", ["连接很紧"], "wet"),
    ("19_跟注者可能更容易中", "跟注者也容易中", ["小对子", "同花连张", "连接牌"], "caller_hits"),
    ("20_故事不自然", "我很强？", ["故事没那么自然"], "question_story"),
    ("21_看对手人数", "人数很重要", ["单挑", "多人"], "people"),
    ("22_单挑更容易成功", "单挑底池", ["C-bet 更清楚"], "heads_up"),
    ("23_多人底池风险", "多人底池", ["有人可能中牌"], "multiway"),
    ("24_人越多越小心", "人越多", ["越要小心"], "careful"),
    ("25_不只是诈唬", "不只是诈唬", ["价值下注", "诈唬/半诈唬"], "two_purpose"),
    ("26_有强牌拿价值", "有强牌", ["拿价值"], "value"),
    ("27_没中也可能代表范围", "没中也可以代表", ["强范围还在"], "miss_range"),
    ("28_希望对手怎么反应", "先问目的", ["想让对手跟？", "还是弃？"], "reaction"),
    ("29_价值下注目的", "价值下注", ["希望被差牌跟"], "value_goal"),
    ("30_诈唬半诈唬目的", "诈唬/半诈唬", ["希望对手弃牌"], "bluff_goal"),
    ("31_三个问题登场", "先问 3 个问题", ["C-bet 检查清单"], "checklist"),
    ("32_问题一牌面对范围有利吗", "问题一", ["牌面对我的范围有利吗？"], "q1"),
    ("33_问题二人数和命中", "问题二", ["人多吗？像中牌吗？"], "q2"),
    ("34_问题三下注目的", "问题三", ["拿价值？", "让对手弃牌？"], "q3"),
    ("35_小口诀", "小口诀", ["翻前我主动，翻后可继续", "牌面讲得通，才是好 C-bet"], "slogan"),
    ("36_下期预告干燥湿润牌面", "下期预告", ["干燥牌面", "湿润牌面"], "next"),
    ("37_合规结尾理性观看", "知识科普", ["娱乐假设", "不宣传赌博", "理性观看"], "end"),
]


def draw_scene(i, stem, title, lines, kind):
    im = base(i * 19)
    d = ImageDraw.Draw(im)
    header(d, title, lines[0] if kind == "title" else None)

    if kind in {"intro", "definition", "story", "range_story", "not_must", "choices", "uncomfortable", "question_story", "careful", "reaction", "checklist", "q3", "slogan", "next", "end"}:
        board(d, title, lines)
        table(d)
        shark(d, 130, 930, 0.95, "wave" if kind in {"intro", "end"} else "point")
        girl(d, 750, 930, 0.85, True)
    elif kind == "title":
        label(d, (260, 370, 820, 485), "continuation bet", size=42)
        label(d, (365, 540, 715, 650), "C-bet", color=(255, 235, 105), txt=(20, 55, 150), size=54)
        table(d)
        shark(d, 120, 790, 1.25, "wave")
        girl(d, 720, 790, 1.05, True)
    elif kind in {"open", "call", "flop_bet"}:
        table(d)
        if kind == "flop_bet":
            flop(d)
            label(d, (360, 750, 720, 835), "bet")
            arrow(d, (540, 930), (540, 820), (48, 105, 205), 14)
        else:
            card_back(im, 245, 525, -6, 1.1)
            card_back(im, 390, 525, 5, 1.1)
            label(d, (315, 760, 765, 850), lines[0], size=42)
            arrow(d, (540, 900), (540, 780), (48, 105, 205), 14)
            chip(d, 505, 920, 34)
            chip(d, 565, 920, 34)
        shark(d, 130, 940, 0.95)
        girl(d, 755, 940, 0.85, True)
    elif kind in {"not_hit", "auto"}:
        board(d, title, lines)
        label(d, (345, 900, 735, 1000), "自动按钮？" if kind == "auto" else "没中也可能下注")
        rounded(d, (430, 1040, 650, 1210), fill=(255, 230, 230), outline=(165, 55, 55), width=7, radius=36)
        center_text(d, (430, 1040, 650, 1210), "C-bet", font(46), (170, 50, 50))
        shark(d, 130, 1120, 0.85)
        girl(d, 760, 1080, 0.85, True)
    elif kind in {"good_board", "dry"}:
        board(d, title, lines)
        flop(d, ("A", "7", "2"), ("♥", "♣", "♦"), 900)
        label(d, (365, 1140, 715, 1225), "比较干燥")
        shark(d, 135, 1140, 0.8)
    elif kind == "scale_range":
        board(d, title, lines)
        rounded(d, (160, 900, 480, 1090), fill=(238, 248, 255), outline=(45, 90, 160), width=6, radius=32)
        rounded(d, (600, 940, 920, 1090), fill=(255, 244, 230), outline=(190, 75, 55), width=6, radius=32)
        center_text(d, (170, 915, 470, 1070), "加注者\n范围", font(40), (30, 80, 165))
        center_text(d, (610, 955, 910, 1070), "跟注者\n范围", font(40), (170, 70, 55))
        d.line((230, 1140, 870, 1185), fill=(45, 45, 45), width=10)
    elif kind == "strong_hands":
        board(d, title, ["这些牌故事更顺"])
        for x, txt in [(170, "AK"), (380, "AQ"), (590, "AA"), (800, "KK")]:
            label(d, (x, 910, x + 145, 1010), txt, color=(238, 248, 255), txt=(20, 70, 150), size=42)
        flop(d, ("A", "7", "2"), ("♥", "♣", "♦"), 1110)
    elif kind == "wet":
        board(d, title, lines)
        flop(d, ("8", "7", "6"), ("♠", "♥", "♣"), 900)
        arrow(d, (350, 1145), (730, 1145), (205, 90, 70), 12)
        label(d, (360, 1195, 720, 1280), "连接很紧")
    elif kind == "caller_hits":
        board(d, title, lines)
        for x, txt in [(165, "小对子"), (415, "同花连张"), (705, "连接牌")]:
            label(d, (x, 930, x + 210, 1030), txt, color=(255, 244, 230), txt=(160, 70, 55), size=34)
        girl(d, 760, 1100, 0.78, True)
    elif kind in {"people", "heads_up", "multiway"}:
        board(d, title, lines)
        table(d)
        count = 2 if kind == "heads_up" else 4 if kind == "multiway" else 3
        for idx in range(count):
            x = 220 + idx * 210
            d.ellipse((x, 925, x + 90, 1015), fill=(238, 248, 255), outline=(35, 35, 35), width=5)
        label(d, (300, 760, 780, 845), lines[0])
    elif kind == "two_purpose":
        label(d, (135, 400, 500, 570), lines[0], color=(238, 248, 255), txt=(20, 70, 150), size=42)
        label(d, (580, 400, 945, 570), lines[1], color=(255, 244, 230), txt=(165, 70, 55), size=42)
        label(d, (180, 690, 900, 790), "C-bet 可以有不同目的")
        table(d)
        shark(d, 145, 910, 0.9)
        girl(d, 760, 910, 0.82, True)
    elif kind in {"value", "miss_range", "value_goal", "bluff_goal"}:
        board(d, title, lines)
        if kind in {"value", "value_goal"}:
            card(d, (365, 900, 515, 1110), "A", "♥", big=True)
            card(d, (565, 900, 715, 1110), "K", "♣", big=True)
            label(d, (350, 1160, 730, 1245), "希望差牌跟")
        else:
            card(d, (365, 900, 515, 1110), "Q", "♣", big=True)
            card(d, (565, 900, 715, 1110), "J", "♠", big=True)
            label(d, (350, 1160, 730, 1245), "希望对手弃")
        shark(d, 145, 1100, 0.8)
    elif kind in {"q1", "q2"}:
        board(d, title, lines)
        if kind == "q1":
            flop(d, ("A", "7", "2"), ("♥", "♣", "♦"), 900)
            flop(d, ("8", "7", "6"), ("♠", "♥", "♣"), 1160)
        else:
            label(d, (150, 925, 450, 1025), "单挑")
            label(d, (620, 925, 920, 1025), "多人")
            d.ellipse((250, 1090, 330, 1170), fill=(238, 248, 255), outline=(35, 35, 35), width=5)
            for x in [650, 750, 850]:
                d.ellipse((x, 1090, x + 80, 1170), fill=(255, 244, 230), outline=(35, 35, 35), width=5)

    final = im.convert("RGB")
    OUT.mkdir(parents=True, exist_ok=True)
    final.save(OUT / f"{stem}_1080x1920.png", quality=95)
    final.save(OUT / f"{stem}_原图.png", quality=95)


def make_preview(start, end):
    imgs = []
    for idx in range(start, end + 1):
        stem = SCENES[idx - 1][0]
        imgs.append(Image.open(OUT / f"{stem}_1080x1920.png"))
    tw, th = 216, 384
    label_h = 70
    canvas = Image.new("RGB", (tw * len(imgs), th + label_h), (245, 240, 230))
    d = ImageDraw.Draw(canvas)
    for offset, img in enumerate(imgs):
        canvas.paste(img.resize((tw, th), Image.Resampling.LANCZOS), (tw * offset, 0))
        center_text(d, (tw * offset, th, tw * (offset + 1), th + label_h), f"{start + offset:02d}", font(34, False), (45, 45, 45))
    REVIEW.mkdir(parents=True, exist_ok=True)
    canvas.save(REVIEW / f"{start:02d}-{end:02d}_preview.png", quality=95)


def main():
    for i, spec in enumerate(SCENES, 1):
        draw_scene(i, *spec)
    for start in range(1, len(SCENES) + 1, 5):
        make_preview(start, min(start + 4, len(SCENES)))


if __name__ == "__main__":
    main()
