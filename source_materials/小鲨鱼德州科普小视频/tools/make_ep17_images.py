from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / "17_什么是被压制dominated"
OUT = EP / "01_手绘图片"
REVIEW = EP / "_style_review"

FONT_BOLD = Path("C:/Windows/Fonts/NotoSansSC-VF.ttf")
FONT_REG = Path("C:/Windows/Fonts/msyh.ttc")

W, H = 1080, 1920
SAFE_TEXT_BOTTOM = 1450


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


def draw_paper_texture(im, seed):
    random.seed(seed)
    px = im.load()
    for _ in range(4200):
        x = random.randrange(W)
        y = random.randrange(H)
        r, g, b = px[x, y][:3]
        delta = random.choice([-4, -3, 3, 4])
        px[x, y] = (max(0, min(255, r + delta)), max(0, min(255, g + delta)), max(0, min(255, b + delta)))


def base(seed=1):
    im = Image.new("RGB", (W, H), (255, 252, 244))
    d = ImageDraw.Draw(im)
    draw_paper_texture(im, seed)
    for x, y, a in [(78, 1545, -12), (860, 1470, 11), (820, 1665, -8), (70, 1700, 9)]:
        card_back(im, x, y, angle=a, scale=0.85)
    for x, y in [(170, 1585), (245, 1625), (755, 1565), (835, 1615), (900, 1710)]:
        chip(d, x, y, 38)
    for x, y in [(125, 260), (945, 330), (175, 1030), (918, 980)]:
        star(d, x, y, 18, fill=(255, 218, 88))
    return im


def star(d, x, y, r, fill):
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
    if pose == "point":
        d.line((x + 168 * s, y + 92 * s, x + 245 * s, y + 55 * s), fill=outline, width=int(7 * s))
    else:
        d.line((x + 32 * s, y + 92 * s, x - 35 * s, y + 50 * s), fill=outline, width=int(7 * s))
        d.line((x + 158 * s, y + 92 * s, x + 225 * s, y + 50 * s), fill=outline, width=int(7 * s))


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
    center_text(d, (95, 82, 985, 182), text, font(60), (19, 70, 160), sw=2)
    if sub:
        center_text(d, (95, 175, 985, 242), sub, font(34, False), (55, 90, 145))


def board(d, title, lines):
    rounded(d, (100, 300, 980, 860), fill=(43, 116, 82), outline=(47, 36, 28), width=9, radius=30)
    center_text(d, (130, 325, 950, 430), title, font(48), (255, 249, 210), (20, 20, 20), 2)
    y = 470
    for line in lines:
        rounded(d, (165, y, 915, y + 84), fill=(250, 255, 250), outline=(35, 35, 35), width=4, radius=20)
        center_text(d, (175, y + 5, 905, y + 79), line, font(36), (35, 65, 55))
        y += 112


def comparison_cards(d, left, right, title=None):
    if title:
        center_text(d, (120, 300, 960, 390), title, font(50), (35, 35, 35), sw=2)
    card(d, (190, 500, 345, 720), left[0], left[1], big=True)
    card(d, (365, 500, 520, 720), left[2], left[3], big=True)
    center_text(d, (500, 555, 580, 655), "vs", font(42), (40, 40, 40))
    card(d, (605, 500, 760, 720), right[0], right[1], big=True)
    card(d, (780, 500, 935, 720), right[2], right[3], big=True)


def label(d, box, text, color=(255, 248, 210), txt=(35, 35, 35)):
    rounded(d, box, fill=color, outline=(35, 35, 35), width=5, radius=22)
    center_text(d, box, text, font(34), txt)


SCENES = [
    ("01_开场为什么中了也难受", "为什么中了\n也难受？", ["上一期：中了也可能多输", "这期：被压制"], "intro"),
    ("02_主题被压制dominated", "被压制", ["dominated"], "title"),
    ("03_不是完全没希望", "不是没希望", ["只是要看对手"], "simple"),
    ("04_同一类牌但更小", "同样中牌", ["我也中了", "对手更大"], "lanes"),
    ("05_弱A例子", "弱 A 例子", ["A7 登场"], "weak_a"),
    ("06_A7对AQ", "A7 vs AQ", [], "a7_aq"),
    ("07_翻牌来了A", "翻牌来了 A", ["两边都一对 A"], "flop_a"),
    ("08_7比Q小", "7 比 Q 小", ["踢脚差距"], "scale_7q"),
    ("09_踢脚kicker", "踢脚", ["kicker"], "kicker"),
    ("10_AQ压着A7", "同样一对 A", ["AQ 往往压着 A7"], "cover"),
    ("11_被压制的味道", "被压制？", ["A7 有点难受"], "bubble"),
    ("12_我也有A误会", "我也有 A", ["先比较"], "mistake"),
    ("13_可以开心中牌", "可以开心", ["但别停在这里"], "happy"),
    ("14_还要问踢脚", "踢脚够好吗？", ["再问一句"], "magnify"),
    ("15_赢小输大", "赢小 输大？", ["小赢", "大输"], "bags"),
    ("16_麻烦点总结", "被压制的麻烦", ["中牌", "踢脚小", "难放手"], "board3"),
    ("17_不是每次都害怕", "不是每次都怕", ["看情况"], "cross"),
    ("18_别只看A", "别只看 A", ["两张牌都要看"], "two_cards"),
    ("19_不只发生在A", "不只发生在 A", ["A", "K", "Q"], "three_cards"),
    ("20_K9对KQ_Q8对QJ", "类似例子", ["K9 vs KQ", "Q8 vs QJ"], "two_matchups"),
    ("21_顶对踢脚不同", "顶对相同", ["踢脚不同"], "top_pair"),
    ("22_平静牌面看踢脚", "牌面越平静", ["越要看踢脚"], "calm"),
    ("23_小同花遇大同花", "小同花", ["也可能遇大同花"], "flush_small"),
    ("24_大同花压小同花", "同类也比大小", ["大同花 > 小同花"], "flush_big"),
    ("25_三个问题登场", "先问 3 个问题", ["检查清单"], "checklist"),
    ("26_问题一只变一对", "问题一", ["中牌后常是一对？"], "q1"),
    ("27_问题二踢脚够好吗", "问题二", ["踢脚够好吗？"], "q2"),
    ("28_问题三更大同类牌", "问题三", ["对手会有更大同类吗？"], "q3"),
    ("29_不舒服就谨慎", "不舒服", ["就谨慎一点"], "cautious"),
    ("30_谨慎不等于一定弃牌", "谨慎不等于弃牌", ["看整体情况"], "fork"),
    ("31_别只靠我也中了", "别只靠", ["我也中了"], "compare"),
    ("32_小口诀", "小口诀", ["同样中牌，比谁更大", "同样一对，看踢脚"], "slogan"),
    ("33_不错却难受", "看起来不错", ["玩起来难受？"], "thinking"),
    ("34_少掉中了却输更多", "开始复盘", ["少掉：明明中了却输更多"], "review"),
    ("35_下期预告持续下注", "下期预告", ["持续下注", "continuation bet"], "next"),
    ("36_合规结尾理性观看", "知识科普", ["娱乐假设", "不宣传赌博", "理性观看"], "end"),
]


def render_scene(i, stem, title, lines, kind):
    im = base(i * 17)
    d = ImageDraw.Draw(im)
    if kind == "title":
        header(d, title, lines[0])
        table(d)
        shark(d, 120, 780, 1.35, "wave")
        girl(d, 720, 760, 1.1, True)
    elif kind == "a7_aq":
        header(d, title)
        comparison_cards(d, ("A", "♠", "7", "♦"), ("A", "♥", "Q", "♣"))
        label(d, (435, 760, 645, 840), "教学例子")
        table(d)
        shark(d, 140, 835, 1.0)
    elif kind == "flop_a":
        header(d, title)
        table(d)
        card(d, (310, 500, 455, 710), "A", "♥", big=True)
        card_back(im, 475, 505, -3, 1.05)
        card_back(im, 640, 505, 4, 1.05)
        label(d, (150, 795, 455, 880), "我：一对 A", (238, 248, 255), (18, 70, 150))
        label(d, (625, 795, 930, 880), "对手：一对 A", (255, 242, 230), (180, 60, 40))
        girl(d, 130, 930, 0.9)
        shark(d, 755, 920, 0.9)
    elif kind == "scale_7q":
        header(d, title)
        d.line((240, 720, 840, 650), fill=(45, 45, 45), width=10)
        d.polygon([(530, 660), (590, 660), (560, 850)], fill=(220, 220, 220), outline=(45, 45, 45))
        card(d, (190, 790, 330, 980), "7", "♦", big=True)
        card(d, (730, 700, 870, 890), "Q", "♣", big=True)
        label(d, (665, 965, 940, 1045), "Q 更大")
        shark(d, 110, 1080, 0.85)
    elif kind == "kicker":
        header(d, title, lines[0])
        card(d, (285, 450, 455, 690), "A", "♠", big=True)
        card(d, (505, 450, 675, 690), "7", "♦", big=True)
        d.ellipse((480, 425, 705, 715), outline=(240, 170, 55), width=14)
        label(d, (415, 770, 775, 855), "旁边这张：踢脚")
        shark(d, 150, 910, 1.0)
        girl(d, 760, 910, 0.9, True)
    elif kind == "cover":
        header(d, title)
        card(d, (285, 560, 425, 755), "A", "♠")
        card(d, (440, 560, 580, 755), "7", "♦")
        card(d, (500, 470, 665, 700), "A", "♥", fill=(255, 244, 224), big=True)
        card(d, (685, 470, 850, 700), "Q", "♣", fill=(255, 244, 224), big=True)
        label(d, (375, 805, 735, 890), "AQ 压着 A7")
        table(d)
    elif kind in ["board3", "intro"]:
        header(d, title)
        board(d, lines[0] if kind == "intro" else title, lines if kind == "intro" else lines)
        shark(d, 135, 930, 1.0)
        girl(d, 735, 930, 0.9, True)
    elif kind == "lanes":
        header(d, title)
        rounded(d, (130, 430, 480, 830), fill=(238, 248, 255), outline=(45, 90, 160), width=6, radius=36)
        rounded(d, (600, 430, 950, 830), fill=(255, 242, 230), outline=(190, 75, 55), width=6, radius=36)
        center_text(d, (145, 450, 465, 620), lines[0], font(45), (30, 80, 165))
        center_text(d, (615, 450, 935, 620), lines[1], font(45), (185, 55, 45))
        d.line((305, 660, 305, 790), fill=(70, 140, 220), width=12)
        d.line((775, 660, 775, 790), fill=(225, 110, 80), width=20)
        girl(d, 420, 930, 1.0, True)
    elif kind in ["weak_a", "two_cards"]:
        header(d, title)
        card(d, (310, 465, 480, 705), "A", "♠", big=True)
        card(d, (545, 465, 715, 705), "7", "♦", big=True)
        label(d, (330, 760, 700, 845), lines[0])
        table(d)
        shark(d, 145, 880, 0.95)
    elif kind == "two_matchups":
        header(d, title)
        comparison_cards(d, ("K", "♠", "9", "♦"), ("K", "♥", "Q", "♣"))
        comparison_cards(d, ("Q", "♦", "8", "♠"), ("Q", "♥", "J", "♣"), None)
        label(d, (230, 850, 850, 930), "都要小心踢脚")
    elif kind in ["q1", "q2", "q3", "checklist"]:
        header(d, title)
        board(d, "检查清单", lines)
        if kind == "q2":
            comparison_cards(d, ("A", "♠", "7", "♦"), ("A", "♥", "Q", "♣"))
        elif kind == "q3":
            card(d, (345, 900, 465, 1065), "6", "♠")
            card(d, (485, 900, 605, 1065), "J", "♠")
            card(d, (625, 900, 745, 1065), "A", "♠")
        girl(d, 765, 1025, 0.8, True)
    elif kind in ["slogan", "end"]:
        header(d, title)
        board(d, title, lines)
        shark(d, 150, 930, 1.05, "wave")
        girl(d, 730, 930, 0.9)
    elif kind in ["flush_small", "flush_big"]:
        header(d, title)
        suits = [("5", "♠"), ("8", "♠"), ("J", "♠"), ("A", "♠")]
        x = 180
        for rank, suit in suits:
            card(d, (x, 500, x + 125, 680), rank, suit)
            x += 155
        label(d, (225, 760, 855, 850), lines[0])
        shark(d, 150, 930, 0.95)
    elif kind == "bags":
        header(d, title)
        rounded(d, (190, 475, 445, 760), fill=(235, 248, 255), outline=(45, 80, 130), width=7, radius=70)
        rounded(d, (620, 420, 900, 805), fill=(255, 236, 224), outline=(170, 65, 50), width=7, radius=80)
        center_text(d, (200, 520, 435, 680), lines[0], font(46), (25, 80, 160))
        center_text(d, (635, 505, 885, 680), lines[1], font(54), (180, 50, 45))
        for x, y, r in [(260, 710, 28), (335, 715, 28), (705, 745, 36), (790, 740, 36), (840, 690, 36)]:
            chip(d, x, y, r)
    elif kind in ["cross", "cautious", "fork", "compare", "thinking", "review", "next", "simple", "bubble", "mistake", "happy", "magnify", "calm", "top_pair", "three_cards"]:
        header(d, title)
        board(d, title, lines)
        table(d)
        if kind == "three_cards":
            for x, rank in [(250, "A"), (470, "K"), (690, "Q")]:
                card(d, (x, 890, x + 150, 1100), rank, "♠", big=True)
        elif kind == "top_pair":
            card(d, (270, 900, 410, 1090), "K", "♠")
            card(d, (465, 900, 605, 1090), "9", "♦")
            card(d, (675, 900, 815, 1090), "Q", "♣")
        elif kind in ["mistake", "happy"]:
            card(d, (455, 900, 625, 1140), "A", "♥", big=True)
        shark(d, 125, 930, 0.95)
        girl(d, 760, 930, 0.85, True)
    else:
        header(d, title)
        board(d, title, lines)
        shark(d, 135, 930, 1.0)
        girl(d, 735, 930, 0.9, True)

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
    cols = len(imgs)
    label_h = 70
    canvas = Image.new("RGB", (tw * cols, th + label_h), (245, 240, 230))
    d = ImageDraw.Draw(canvas)
    for offset, img in enumerate(imgs):
        canvas.paste(img.resize((tw, th), Image.Resampling.LANCZOS), (tw * offset, 0))
        center_text(d, (tw * offset, th, tw * (offset + 1), th + label_h), f"{start + offset:02d}", font(34, False), (45, 45, 45))
    REVIEW.mkdir(parents=True, exist_ok=True)
    canvas.save(REVIEW / f"{start:02d}-{end:02d}_preview.png", quality=95)


def main():
    for i, spec in enumerate(SCENES, 1):
        render_scene(i, *spec)
    for start in [1, 6, 11, 16, 21, 26]:
        make_preview(start, start + 4)
    make_preview(31, len(SCENES))


if __name__ == "__main__":
    main()
