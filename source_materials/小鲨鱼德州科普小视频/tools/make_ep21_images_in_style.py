from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
EP21 = ROOT / "21_什么是半诈唬semi_bluff"
OUT = EP21 / "01_手绘图片"
REVIEW = EP21 / "_style_review"

FONT_BOLD = Path("C:/Windows/Fonts/NotoSansSC-VF.ttf")
FONT_REG = Path("C:/Windows/Fonts/msyh.ttc")

W, H = 1080, 1920
NAVY = (8, 34, 145)
INK = (28, 32, 48)
GREEN = (96, 158, 116)
FELT = (67, 139, 98)
SKY = (196, 232, 255)
YELLOW = (255, 232, 92)
CREAM = (255, 250, 226)
PINK = (255, 215, 224)
RED = (218, 63, 75)
BLUE = (63, 134, 218)
PALE = (248, 252, 255)


SCENES = [
    ("01_开场衔接Cbet尺度", "上一期：C-bet 尺度", ["下一步？", "半诈唬"], "intro"),
    ("02_主题半诈唬", "半诈唬？", ["semi-bluff"], "girl_question"),
    ("03_术语SemiBluff", "semi-bluff", ["半诈唬"], "blackboard"),
    ("04_不是乱吓人", "不是乱吓人", ["先看机会"], "cross_note"),
    ("05_现在不是最好牌", "还没完成", ["现在可能不是最好牌"], "puzzle"),
    ("06_同花听牌例子", "同花听牌", ["两张同花", "还差一张"], "flush_draw"),
    ("07_翻牌两张同花", "两张同花", ["用放大镜看牌面"], "magnifier_board"),
    ("08_还没有成牌", "现在还没成牌", ["高牌 / 未完成"], "now_not_made"),
    ("09_后面可能完成", "可能变强", ["转牌 / 河牌"], "future_card"),
    ("10_主动下注", "主动下注", ["带着听牌的小筹码"], "bet_draw"),
    ("11_不同于纯诈唬", "不一样", ["纯诈唬", "半诈唬"], "compare"),
    ("12_纯诈唬依赖弃牌", "纯诈唬", ["更依赖马上弃牌"], "single_path"),
    ("13_保留改进机会", "保留机会", ["弃牌", "变强"], "two_paths"),
    ("14_两条路概念", "两条路", ["现在赢", "后面变强"], "road_sign"),
    ("15_对手现在弃牌", "现在弃牌", ["当前底池"], "fold_now"),
    ("16_被跟注后变强", "下一页变强", ["被跟注后仍有机会"], "story_page"),
    ("17_不是没牌敢打", "不是硬打", ["没牌也敢打？"], "wrong_idea"),
    ("18_后续可能性", "后续可能性", ["听牌", "outs", "后续牌"], "chain_cards"),
    ("19_同花听牌牌型", "同花听牌", ["水滴", "同花图标"], "still_life_flush"),
    ("20_顺子听牌牌型", "顺子听牌", ["差一张连上"], "straight_draw"),
    ("21_后门听牌和范围", "后门机会", ["范围故事"], "backdoor_range"),
    ("22_不是所有听牌适合", "先检查", ["不是所有听牌都适合"], "sort_draws"),
    ("23_outs多不多", "outs 多不多？", ["补牌计数"], "outs_count"),
    ("24_对手会不会弃牌", "会不会弃牌？", ["观察对手"], "opponent_fold"),
    ("25_不爱弃牌压力小", "压力变小", ["对手不爱弃牌"], "sticky_opponent"),
    ("26_牌面故事合理吗", "故事合理吗？", ["牌面 + 范围"], "story_reason"),
    ("27_A高干燥牌面", "A 高干燥", ["A 7 2", "范围较亮"], "dry_a72"),
    ("28_小额Cbet代表范围", "容易讲通", ["小额 C-bet", "强范围"], "small_cbet_story"),
    ("29_湿润多人牌面", "湿润多人", ["8 7 6", "连接很多"], "wet_multi"),
    ("30_继续理由变多", "继续理由变多", ["一对", "听顺", "听花"], "continue_reasons"),
    ("31_更谨慎", "更谨慎", ["先想清楚"], "careful_button"),
    ("32_不是听牌必下注", "不是必下注", ["听牌 = 必下注？"], "not_must_bet"),
    ("33_过牌控池也合适", "看情况", ["过牌", "控池", "看下一张"], "options_fan"),
    ("34_两种赢法检查", "两种赢法", ["现在弃牌", "后面变强"], "check_two_ways"),
    ("35_两条赢法合并图", "两条赢法", ["左：弃牌", "右：变强"], "combined_win"),
    ("36_小口诀", "小口诀", ["不是空喊吓人", "带着机会讲故事"], "slogan"),
    ("37_下期预告弃牌率", "下期预告", ["弃牌率", "fold equity"], "next"),
    ("38_合规结尾理性观看", "知识科普", ["娱乐假设", "不宣传赌博", "理性观看"], "end"),
]


def font(size, bold=True):
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REG
    return ImageFont.truetype(str(path), size)


def text_size(draw, text, fnt, sw=0):
    box = draw.textbbox((0, 0), text, font=fnt, stroke_width=sw)
    return box[2] - box[0], box[3] - box[1]


def center_text(draw, box, text, fnt, fill=NAVY, stroke=(255, 255, 255), sw=0, gap=8):
    lines = text.split("\n")
    sizes = [text_size(draw, line, fnt, sw) for line in lines]
    total_h = sum(h for _, h in sizes) + gap * (len(lines) - 1)
    y = box[1] + (box[3] - box[1] - total_h) / 2
    for line, (tw, th) in zip(lines, sizes):
        x = box[0] + (box[2] - box[0] - tw) / 2
        draw.text((x, y), line, font=fnt, fill=fill, stroke_width=sw, stroke_fill=stroke)
        y += th + gap


def rounded(draw, box, fill, outline=INK, width=6, radius=28):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def label(draw, box, text, fill=CREAM, size=38, txt=NAVY):
    rounded(draw, box, fill, width=5, radius=20)
    center_text(draw, box, text, font(size), txt, sw=1)


def doodle_bg(draw, seed):
    random.seed(seed)
    for _ in range(70):
        x, y = random.randint(20, W - 20), random.randint(30, H - 40)
        if 1430 < y < 1880:
            continue
        c = random.choice([(210, 236, 255), (255, 240, 145), (225, 244, 230)])
        if random.random() < 0.35:
            draw.ellipse((x, y, x + 9, y + 9), outline=c, width=2)
        elif random.random() < 0.65:
            draw.line((x, y, x + 18, y + 12), fill=c, width=3)
        else:
            draw.text((x, y), random.choice(["♠", "♥", "♦", "♣"]), font=font(24), fill=c)


def make_canvas(seed):
    im = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(im)
    doodle_bg(d, seed)
    d.rounded_rectangle((38, 36, 1042, 1848), radius=42, outline=(229, 237, 248), width=5)
    return im, d


def title_block(draw, title, idx):
    rounded(draw, (72, 66, 1008, 302), (255, 255, 255), outline=(18, 28, 70), width=8, radius=48)
    draw.arc((170, 226, 910, 320), 185, 355, fill=(242, 190, 30), width=8)
    clean = title.replace("\n", "")
    size = 78 if len(clean) <= 7 else 66 if len(clean) <= 11 else 54
    center_text(draw, (112, 94, 968, 266), title, font(size), NAVY, sw=3)
    label(draw, (812, 84, 965, 148), "第21期", fill=YELLOW, size=30)


def table(draw, box=(105, 785, 975, 1375)):
    draw.ellipse(box, fill=FELT, outline=INK, width=8)
    inner = (box[0] + 42, box[1] + 42, box[2] - 42, box[3] - 42)
    draw.ellipse(inner, outline=(200, 242, 218), width=5)


def card(draw, x, y, text, suit=None, scale=1.0, fill=(255, 255, 255), tilt=0):
    w, h = int(116 * scale), int(158 * scale)
    rounded(draw, (x, y, x + w, y + h), fill, outline=INK, width=max(3, int(5 * scale)), radius=int(16 * scale))
    if suit:
        color = RED if suit in ["♥", "♦"] else INK
        center_text(draw, (x + 8, y + 22, x + w - 8, y + h - 14), f"{text}\n{suit}", font(int(40 * scale)), color, sw=1, gap=4)
    else:
        center_text(draw, (x + 8, y + 22, x + w - 8, y + h - 14), text, font(int(40 * scale)), NAVY, sw=1, gap=4)


def chip(draw, x, y, r=38, color=BLUE):
    draw.ellipse((x - r, y - r, x + r, y + r), fill=(245, 252, 255), outline=INK, width=5)
    draw.ellipse((x - r + 10, y - r + 10, x + r - 10, y + r - 10), fill=color, outline=INK, width=3)
    draw.ellipse((x - 13, y - 13, x + 13, y + 13), fill=(255, 255, 255), outline=INK, width=2)


def chips(draw, cx, cy, n=4):
    for i in range(n):
        chip(draw, cx + i * 23, cy - i * 10, 36, BLUE if i % 2 else (90, 170, 230))


def arrow(draw, start, end, fill=BLUE, width=10):
    draw.line((*start, *end), fill=fill, width=width)
    ang = math.atan2(end[1] - start[1], end[0] - start[0])
    a1, a2 = ang + 2.55, ang - 2.55
    pts = [
        end,
        (end[0] + 34 * math.cos(a1), end[1] + 34 * math.sin(a1)),
        (end[0] + 34 * math.cos(a2), end[1] + 34 * math.sin(a2)),
    ]
    draw.polygon(pts, fill=fill, outline=INK)


def shark(draw, x, y, s=1.0, mood="happy"):
    body = (x, y, x + int(210 * s), y + int(150 * s))
    draw.ellipse(body, fill=(156, 218, 245), outline=INK, width=max(4, int(6 * s)))
    draw.polygon([(x + int(78 * s), y + int(8 * s)), (x + int(122 * s), y - int(66 * s)), (x + int(154 * s), y + int(14 * s))], fill=(156, 218, 245), outline=INK)
    draw.ellipse((x + int(55 * s), y + int(42 * s), x + int(75 * s), y + int(62 * s)), fill=INK)
    draw.ellipse((x + int(132 * s), y + int(42 * s), x + int(152 * s), y + int(62 * s)), fill=INK)
    if mood == "think":
        draw.arc((x + int(78 * s), y + int(78 * s), x + int(135 * s), y + int(120 * s)), 200, 340, fill=INK, width=max(3, int(5 * s)))
    else:
        draw.arc((x + int(76 * s), y + int(76 * s), x + int(138 * s), y + int(118 * s)), 10, 170, fill=INK, width=max(3, int(5 * s)))
    draw.polygon([(x + int(198 * s), y + int(68 * s)), (x + int(252 * s), y + int(36 * s)), (x + int(244 * s), y + int(110 * s))], fill=(156, 218, 245), outline=INK)
    draw.ellipse((x + int(40 * s), y + int(85 * s), x + int(72 * s), y + int(116 * s)), fill=(255, 173, 190))


def girl(draw, x, y, s=1.0, mood="question"):
    draw.ellipse((x + int(28 * s), y + int(46 * s), x + int(220 * s), y + int(250 * s)), fill=(49, 48, 60), outline=INK, width=max(4, int(6 * s)))
    draw.ellipse((x + int(48 * s), y + int(34 * s), x + int(206 * s), y + int(204 * s)), fill=(255, 226, 206), outline=INK, width=max(4, int(6 * s)))
    draw.pieslice((x + int(48 * s), y + int(5 * s), x + int(206 * s), y + int(118 * s)), 180, 360, fill=SKY, outline=INK, width=max(4, int(5 * s)))
    draw.polygon([(x + int(118 * s), y + int(6 * s)), (x + int(154 * s), y - int(54 * s)), (x + int(175 * s), y + int(22 * s))], fill=SKY, outline=INK)
    draw.ellipse((x + int(88 * s), y + int(104 * s), x + int(106 * s), y + int(126 * s)), fill=INK)
    draw.ellipse((x + int(146 * s), y + int(104 * s), x + int(164 * s), y + int(126 * s)), fill=INK)
    draw.ellipse((x + int(70 * s), y + int(135 * s), x + int(100 * s), y + int(158 * s)), fill=(255, 156, 174))
    draw.ellipse((x + int(154 * s), y + int(135 * s), x + int(184 * s), y + int(158 * s)), fill=(255, 156, 174))
    if mood == "question":
        center_text(draw, (x + int(100 * s), y + int(148 * s), x + int(160 * s), y + int(196 * s)), "?", font(int(42 * s)), INK)
    else:
        draw.arc((x + int(100 * s), y + int(146 * s), x + int(156 * s), y + int(184 * s)), 15, 165, fill=INK, width=max(3, int(5 * s)))
    rounded(draw, (x + int(58 * s), y + int(220 * s), x + int(198 * s), y + int(360 * s)), fill=(225, 238, 255), outline=INK, width=max(4, int(5 * s)), radius=int(24 * s))


def note(draw, box, text, fill=(255, 255, 255), size=42):
    rounded(draw, box, fill, width=5, radius=24)
    center_text(draw, box, text, font(size), NAVY, sw=1, gap=8)


def draw_cross(draw, box):
    draw.line((box[0], box[1], box[2], box[3]), fill=RED, width=16)
    draw.line((box[0], box[3], box[2], box[1]), fill=RED, width=16)


def draw_board_cards(draw, cards, y=820, x0=310, scale=1.05):
    gap = int(135 * scale)
    for i, (rank, suit) in enumerate(cards):
        card(draw, x0 + i * gap, y, rank, suit, scale)


def suit_icon(draw, x, y, suit, size=72):
    color = RED if suit in ["♥", "♦"] else INK
    center_text(draw, (x, y, x + size, y + size), suit, font(size), color, sw=1)


def draw_scene(draw, idx, scene):
    _, title, labels, kind = scene
    title_block(draw, title, idx)

    if kind in {"intro", "girl_question", "blackboard", "cross_note", "wrong_idea", "not_must_bet"}:
        girl(draw, 95, 930, 1.25, "question")
        shark(draw, 680, 970, 1.0, "think")
        note(draw, (195, 425, 885, 640), labels[0], fill=CREAM, size=56)
        if kind in {"cross_note", "wrong_idea", "not_must_bet"}:
            note(draw, (250, 700, 830, 860), labels[-1], fill=(255, 244, 248), size=46)
            draw_cross(draw, (276, 720, 804, 840))
        if kind == "blackboard":
            rounded(draw, (145, 435, 935, 885), fill=(68, 112, 94), outline=INK, width=8, radius=34)
            center_text(draw, (180, 500, 900, 775), "semi-bluff\n半诈唬", font(78), (255, 255, 245), sw=2, gap=22)

    elif kind in {"flush_draw", "magnifier_board", "dry_a72", "wet_multi", "continue_reasons"}:
        table(draw, (95, 675, 985, 1335))
        if kind == "dry_a72":
            draw_board_cards(draw, [("A", "♠"), ("7", "♦"), ("2", "♣")], 850, 305)
            label(draw, (315, 1160, 765, 1250), "范围较亮", fill=YELLOW, size=42)
        elif kind in {"wet_multi", "continue_reasons"}:
            draw_board_cards(draw, [("8", "♥"), ("7", "♥"), ("6", "♣")], 850, 305)
            for x, y in [(205, 700), (850, 720), (190, 1260), (840, 1260)]:
                draw.ellipse((x - 42, y - 42, x + 42, y + 42), fill=(255, 235, 210), outline=INK, width=5)
            if kind == "continue_reasons":
                label(draw, (145, 1375, 360, 1455), "一对", size=36)
                label(draw, (430, 1375, 650, 1455), "听顺", size=36)
                label(draw, (720, 1375, 935, 1455), "听花", size=36)
        else:
            card(draw, 245, 1060, "A", "♥", 1.0)
            card(draw, 382, 1060, "K", "♥", 1.0)
            draw_board_cards(draw, [("9", "♥"), ("4", "♥"), ("2", "♣")], 810, 330)
            arrow(draw, (365, 1040), (440, 965), BLUE, 8)
            arrow(draw, (500, 1040), (535, 965), BLUE, 8)
            label(draw, (320, 1345, 760, 1430), "还差一张同花", fill=CREAM, size=38)
            if kind == "magnifier_board":
                draw.ellipse((190, 650, 445, 905), outline=INK, width=12)
                draw.line((390, 850, 520, 980), fill=INK, width=18)
        shark(draw, 730, 400, 0.72)

    elif kind in {"puzzle", "now_not_made", "future_card"}:
        rounded(draw, (130, 440, 950, 1290), fill=(250, 253, 255), outline=INK, width=7, radius=36)
        if kind == "puzzle":
            for j, col in enumerate([SKY, CREAM, PINK]):
                rounded(draw, (220 + j * 200, 700, 390 + j * 200, 880), col, width=5, radius=22)
            draw.rectangle((590, 736, 705, 850), fill=(255, 255, 255), outline=INK, width=5)
            label(draw, (310, 1030, 770, 1120), labels[0], size=38)
        elif kind == "now_not_made":
            card(draw, 300, 650, "A", "♣", 1.25)
            label(draw, (520, 690, 810, 790), "高牌", fill=CREAM, size=44)
            label(draw, (330, 980, 750, 1075), "同花未点亮", fill=(236, 242, 255), size=40)
        else:
            card(draw, 245, 700, "?", None, 1.25, fill=(230, 244, 255))
            card(draw, 470, 660, "♥", None, 1.35, fill=(255, 245, 250))
            suit_icon(draw, 520, 715, "♥", 92)
            label(draw, (295, 1035, 795, 1128), "可能变强", fill=YELLOW, size=48)
        girl(draw, 765, 1240, 0.75, "smile")

    elif kind in {"bet_draw", "small_cbet_story"}:
        table(draw, (120, 610, 960, 1240))
        draw_board_cards(draw, [("A", "♠"), ("7", "♦"), ("2", "♣")], 785, 335)
        chips(draw, 465, 1080, 5)
        arrow(draw, (470, 1040), (535, 930), BLUE, 9)
        label(draw, (270, 1320, 810, 1410), labels[0], fill=CREAM, size=42)
        shark(draw, 125, 420, 0.78)
        girl(draw, 745, 430, 0.78, "smile")

    elif kind in {"compare", "single_path", "two_paths", "road_sign", "combined_win"}:
        rounded(draw, (90, 435, 990, 1345), fill=PALE, outline=INK, width=7, radius=40)
        if kind == "compare":
            label(draw, (165, 590, 465, 700), "纯诈唬", fill=(255, 238, 238), size=46)
            label(draw, (615, 590, 915, 700), "半诈唬", fill=(225, 246, 255), size=46)
            arrow(draw, (315, 760), (315, 1040), RED, 8)
            arrow(draw, (765, 760), (690, 1010), BLUE, 8)
            arrow(draw, (765, 760), (850, 1010), GREEN, 8)
        elif kind == "single_path":
            arrow(draw, (230, 900), (820, 900), RED, 10)
            label(draw, (625, 785, 900, 1010), "对手弃牌", fill=(255, 238, 238), size=42)
        else:
            arrow(draw, (530, 830), (270, 1110), BLUE, 10)
            arrow(draw, (550, 830), (830, 1110), GREEN, 10)
            label(draw, (135, 1110, 410, 1210), labels[0], size=38)
            label(draw, (670, 1110, 945, 1210), labels[1], fill=(230, 250, 235), size=38)
        shark(draw, 410, 475, 0.85)

    elif kind in {"fold_now", "opponent_fold", "sticky_opponent"}:
        table(draw, (100, 630, 980, 1280))
        chips(draw, 510, 955, 5)
        draw.ellipse((430, 705, 650, 900), fill=(255, 230, 205), outline=INK, width=7)
        if kind == "sticky_opponent":
            rounded(draw, (385, 690, 695, 930), fill=(242, 242, 242), outline=INK, width=6, radius=36)
            label(draw, (305, 1320, 775, 1410), "压力变小", fill=(255, 238, 238), size=46)
            arrow(draw, (280, 1070), (465, 960), fill=(160, 180, 210), width=7)
        else:
            card(draw, 500, 810, "背", None, 0.82, fill=(210, 236, 255))
            label(draw, (300, 1320, 780, 1410), labels[0], fill=CREAM, size=46)
        girl(draw, 110, 420, 0.78, "question")

    elif kind in {"story_page", "story_reason", "backdoor_range"}:
        rounded(draw, (115, 440, 965, 1300), fill=(255, 252, 236), outline=INK, width=7, radius=36)
        draw.line((540, 480, 540, 1260), fill=(230, 210, 168), width=5)
        center_text(draw, (160, 545, 500, 700), "故事线", font(54), NAVY, sw=1)
        arrow(draw, (250, 830), (475, 980), BLUE, 9)
        if kind == "story_page":
            suit_icon(draw, 665, 720, "♥", 100)
            label(draw, (610, 970, 890, 1060), "点亮", fill=YELLOW, size=42)
        else:
            label(draw, (590, 600, 895, 700), labels[0], fill=(236, 246, 255), size=38)
            label(draw, (600, 880, 890, 980), labels[-1], fill=CREAM, size=38)
        shark(draw, 750, 1260, 0.65)

    elif kind in {"chain_cards", "still_life_flush", "straight_draw", "sort_draws", "outs_count"}:
        rounded(draw, (100, 430, 980, 1325), fill=(252, 254, 255), outline=INK, width=7, radius=36)
        if kind == "straight_draw":
            for i, rank in enumerate(["6", "7", "8", "9", "?"]):
                card(draw, 190 + i * 130, 730 + (i % 2) * 45, rank, "♣" if rank != "?" else None, 0.85)
            label(draw, (310, 1080, 770, 1170), "差一张连上", fill=YELLOW, size=46)
        elif kind == "outs_count":
            for i in range(8):
                suit_icon(draw, 205 + (i % 4) * 160, 660 + (i // 4) * 170, random.choice(["♥", "♦", "♠", "♣"]), 82)
            label(draw, (300, 1070, 780, 1160), "补牌计数", fill=CREAM, size=46)
        elif kind == "sort_draws":
            for i in range(5):
                card(draw, 165 + i * 145, 630 + (i % 2) * 80, "听", None, 0.76, fill=(235, 247, 255))
            label(draw, (310, 1050, 770, 1145), "先检查", fill=YELLOW, size=48)
        else:
            items = labels if kind == "chain_cards" else ["水滴", "同花", "放大镜"]
            for i, t in enumerate(items):
                note(draw, (170 + i * 250, 660, 370 + i * 250, 830), t, fill=[SKY, CREAM, PINK][i % 3], size=38)
                if i < len(items) - 1:
                    arrow(draw, (370 + i * 250, 745), (420 + i * 250, 745), GREEN, 7)
            if kind == "still_life_flush":
                suit_icon(draw, 470, 940, "♥", 120)
        girl(draw, 720, 1190, 0.7, "smile")

    elif kind in {"careful_button", "options_fan", "check_two_ways"}:
        girl(draw, 95, 680, 1.1, "question")
        rounded(draw, (475, 670, 865, 980), fill=(255, 244, 248), outline=INK, width=7, radius=36)
        center_text(draw, (505, 735, 835, 900), "BET", font(82), RED, sw=2)
        if kind == "careful_button":
            label(draw, (465, 1110, 880, 1200), "先想清楚", fill=YELLOW, size=46)
            shark(draw, 670, 1200, 0.8, "think")
        elif kind == "options_fan":
            for i, t in enumerate(labels):
                note(draw, (190 + i * 230, 1110 - abs(i - 1) * 60, 390 + i * 230, 1210 - abs(i - 1) * 60), t, fill=[CREAM, SKY, PINK][i], size=34)
        else:
            note(draw, (350, 1080, 790, 1180), labels[0], fill=CREAM, size=38)
            note(draw, (350, 1230, 790, 1330), labels[1], fill=(230, 250, 235), size=38)

    elif kind in {"slogan", "next", "end"}:
        if kind == "slogan":
            rounded(draw, (95, 470, 985, 1120), fill=(255, 255, 255), outline=INK, width=8, radius=68)
            center_text(draw, (150, 580, 930, 1000), "不是空喊吓人\n而是带着机会讲故事", font(68), NAVY, sw=3, gap=28)
            chips(draw, 180, 1340, 4)
            shark(draw, 740, 1280, 0.75)
        elif kind == "next":
            rounded(draw, (130, 500, 950, 1130), fill=(236, 248, 255), outline=INK, width=8, radius=48)
            center_text(draw, (180, 610, 900, 890), "弃牌率\nfold equity", font(82), NAVY, sw=3, gap=22)
            note(draw, (320, 950, 760, 1045), "会不会弃牌？", fill=YELLOW, size=42)
            shark(draw, 400, 1200, 0.9)
        else:
            shark(draw, 170, 760, 1.05)
            girl(draw, 640, 720, 1.05, "smile")
            rounded(draw, (150, 1220, 930, 1455), fill=(68, 112, 94), outline=INK, width=8, radius=34)
            center_text(draw, (185, 1255, 895, 1420), "知识科普  娱乐假设\n不宣传赌博  理性观看", font(48), (255, 255, 245), sw=1, gap=16)

    else:
        note(draw, (190, 620, 890, 850), labels[0], fill=CREAM, size=52)
        shark(draw, 410, 970, 0.95)

    # Bottom-safe decorative band with no text.
    for x in [120, 205, 850, 930]:
        chip(draw, x, 1700 + (x % 3) * 28, 28)
    for x in [320, 470, 615]:
        card(draw, x, 1630, "背", None, 0.52, fill=(210, 236, 255))


def save_scene(idx, scene):
    im, draw = make_canvas(idx)
    draw_scene(draw, idx, scene)
    im = im.convert("RGB")
    name = scene[0]
    src = OUT / f"{name}_v1_原图.png"
    final = OUT / f"{name}_v1_1080x1920.png"
    im.save(src, quality=95)
    im.save(final, quality=95)
    return final


def make_review(paths, start, end):
    thumbs = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        im.thumbnail((216, 384))
        canvas = Image.new("RGB", (216, 384), "white")
        canvas.paste(im, ((216 - im.width) // 2, (384 - im.height) // 2))
        thumbs.append(canvas)
    review = Image.new("RGB", (216 * len(thumbs), 384), (245, 248, 252))
    for i, im in enumerate(thumbs):
        review.paste(im, (i * 216, 0))
    review.save(REVIEW / f"{start:02d}-{end:02d}_preview.png", quality=92)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    paths = []
    for idx, scene in enumerate(SCENES, start=1):
        paths.append(save_scene(idx, scene))
    for start in range(1, len(paths) + 1, 5):
        end = min(start + 4, len(paths))
        make_review(paths[start - 1:end], start, end)
    print(f"Generated {len(paths)} scenes.")
    print("Generated preview contact sheets.")


if __name__ == "__main__":
    main()
