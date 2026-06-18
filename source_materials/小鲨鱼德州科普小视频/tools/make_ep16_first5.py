from pathlib import Path
import shutil

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "_tmp_ep16_refs"
OUT = ROOT / "16_什么是反向隐含赔率reverse_implied_odds" / "01_手绘图片"
REVIEW = ROOT / "16_什么是反向隐含赔率reverse_implied_odds" / "_style_review"

FONT_BOLD = Path("C:/Windows/Fonts/NotoSansSC-VF.ttf")
FONT_REG = Path("C:/Windows/Fonts/msyh.ttc")


def font(size, bold=True):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REG), size)


def draw_center(draw, box, text, fnt, fill, stroke_fill=None, stroke_width=0, line_gap=8):
    lines = text.split("\n")
    widths, heights = [], []
    for line in lines:
        b = draw.textbbox((0, 0), line, font=fnt, stroke_width=stroke_width)
        widths.append(b[2] - b[0])
        heights.append(b[3] - b[1])
    total_h = sum(heights) + line_gap * (len(lines) - 1)
    y = box[1] + ((box[3] - box[1]) - total_h) / 2
    for line, w, h in zip(lines, widths, heights):
        x = box[0] + ((box[2] - box[0]) - w) / 2
        draw.text((x, y), line, font=fnt, fill=fill, stroke_fill=stroke_fill, stroke_width=stroke_width)
        y += h + line_gap


def rounded(draw, box, fill, outline=(20, 20, 20), width=8, radius=34):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def cloud(draw, box, fill=(255, 255, 255), outline=(18, 18, 18), width=8):
    rounded(draw, box, fill, outline, width, radius=44)
    x1, y1, x2, y2 = box
    r = (y2 - y1) // 3
    for cx in [x1 + 70, x1 + 170, x1 + 290, x2 - 120]:
        draw.ellipse((cx - r, y1 - r // 2, cx + r, y1 + r), fill=fill, outline=outline, width=width)


def soft_cover(im, box, color):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, radius=32, fill=color)
    im.alpha_composite(layer)


def add_card_back_doodles(draw):
    # Extra decorative cards use the same pale blue back and tiny shark-face mark.
    for x, y, a in [(72, 1510, -12), (886, 1390, 10), (790, 1630, -8)]:
        card = Image.new("RGBA", (140, 190), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((8, 8, 132, 182), radius=18, fill=(204, 224, 255, 210), outline=(120, 160, 235), width=5)
        cd.ellipse((51, 72, 89, 110), fill=(255, 255, 255, 230), outline=(95, 145, 220), width=3)
        cd.arc((53, 80, 87, 118), 200, 340, fill=(95, 145, 220), width=3)
        rot = card.rotate(a, expand=True, resample=Image.Resampling.BICUBIC)
        draw.bitmap((x, y), rot, fill=None)


def save_pair(im, stem):
    OUT.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    final = im.convert("RGB")
    final.save(OUT / f"{stem}_1080x1920.png", quality=95)
    final.save(OUT / f"{stem}_原图.png", quality=95)


def img01():
    im = Image.open(REF / "ref15_01.png").convert("RGBA")
    d = ImageDraw.Draw(im)
    # Replace chalkboard text, keeping the existing characters and table density.
    rounded(d, (38, 58, 910, 540), fill=(42, 116, 82), outline=(48, 34, 25), width=12, radius=28)
    draw_center(d, (65, 105, 880, 315), "还有反方向？", font(78), (255, 255, 240), (20, 20, 20), 3)
    d.line((150, 348, 800, 332), fill=(234, 247, 255), width=6)
    d.text((130, 388), "reverse implied odds", font=font(34, False), fill=(224, 244, 238))
    rounded(d, (72, 710, 320, 875), fill=(255, 255, 255), outline=(28, 28, 28), width=6, radius=22)
    draw_center(d, (86, 728, 306, 858), "implied odds\n未来可能多赢", font(31), (18, 63, 165), (255, 255, 255), 1)
    save_pair(im, "01_开场还有反方向")


def img02():
    im = Image.open(REF / "ref15_02.png").convert("RGBA")
    d = ImageDraw.Draw(im)
    # Bright, non-table composition: two arrows and richer color accents.
    soft_cover(im, (55, 60, 1015, 670), (255, 255, 255, 255))
    cloud(d, (228, 78, 850, 230))
    draw_center(d, (240, 86, 838, 228), "反方向的问题", font(62), (18, 62, 170), (255, 255, 255), 2)
    d.line((245, 430, 445, 290), fill=(78, 157, 235), width=18)
    d.polygon([(445, 290), (405, 286), (438, 245)], fill=(78, 157, 235))
    d.line((630, 290, 835, 445), fill=(239, 103, 86), width=18)
    d.polygon([(835, 445), (795, 434), (830, 400)], fill=(239, 103, 86))
    rounded(d, (210, 465, 440, 580), fill=(238, 248, 255), outline=(34, 99, 185), width=6, radius=25)
    rounded(d, (650, 465, 885, 580), fill=(255, 242, 238), outline=(205, 67, 61), width=6, radius=25)
    draw_center(d, (210, 470, 440, 575), "多赢？", font(50), (18, 79, 190), (255, 255, 255), 2)
    draw_center(d, (650, 470, 885, 575), "多输？", font(50), (203, 42, 45), (255, 255, 255), 2)
    add_card_back_doodles(d)
    save_pair(im, "02_反方向的问题")


def img03():
    im = Image.open(REF / "ref15_03.png").convert("RGBA")
    d = ImageDraw.Draw(im)
    soft_cover(im, (70, 50, 1045, 675), (255, 255, 255, 255))
    cloud(d, (118, 88, 965, 320))
    draw_center(d, (140, 110, 945, 230), "反向隐含赔率", font(74), (18, 62, 168), (255, 255, 255), 2)
    draw_center(d, (160, 225, 925, 310), "reverse implied odds", font(46), (24, 88, 178), (255, 255, 255), 2)
    rounded(d, (725, 380, 965, 500), fill=(255, 248, 204), outline=(24, 24, 24), width=6, radius=24)
    draw_center(d, (735, 390, 955, 490), "第16期", font(40), (35, 35, 35))
    save_pair(im, "03_主题反向隐含赔率")


def img04():
    im = Image.open(REF / "ref15_05.png").convert("RGBA")
    d = ImageDraw.Draw(im)
    soft_cover(im, (55, 70, 560, 310), (255, 255, 255, 238))
    cloud(d, (70, 80, 545, 220))
    draw_center(d, (82, 82, 532, 218), "普通隐含赔率", font(58), (18, 62, 168), (255, 255, 255), 2)
    rounded(d, (90, 245, 480, 385), fill=(235, 248, 255), outline=(28, 28, 28), width=6, radius=24)
    draw_center(d, (110, 255, 460, 376), "中了以后\n可能多赢", font(45), (18, 77, 180), (255, 255, 255), 2)
    # Add small golden future glow without covering shark-logo cards/chips.
    for r, alpha in [(120, 50), (85, 70), (50, 100)]:
        d.ellipse((795 - r, 295 - r, 795 + r, 295 + r), outline=(255, 203, 62, alpha), width=8)
    save_pair(im, "04_普通隐含赔率看多赢")


def img05():
    im = Image.open(REF / "ref15_05.png").convert("RGBA")
    d = ImageDraw.Draw(im)
    soft_cover(im, (40, 60, 1040, 455), (255, 255, 255, 252))
    cloud(d, (66, 80, 710, 230))
    draw_center(d, (80, 82, 700, 225), "反向隐含赔率", font(62), (168, 42, 55), (255, 255, 255), 2)
    rounded(d, (105, 260, 640, 410), fill=(255, 242, 225), outline=(40, 40, 40), width=7, radius=24)
    draw_center(d, (120, 270, 625, 400), "中了以后\n也可能多输", font(49), (205, 53, 48), (255, 255, 255), 2)
    # Gentle warning sign and question shadow on the future road.
    d.polygon([(790, 530), (910, 745), (670, 745)], fill=(255, 234, 164), outline=(35, 35, 35))
    d.line((790, 585, 790, 670), fill=(205, 53, 48), width=12)
    d.ellipse((780, 690, 800, 710), fill=(205, 53, 48))
    rounded(d, (635, 765, 955, 860), fill=(250, 245, 255), outline=(95, 80, 160), width=5, radius=20)
    draw_center(d, (645, 770, 945, 855), "未来风险？", font(40), (126, 68, 160), (255, 255, 255), 2)
    save_pair(im, "05_反向隐含赔率看多输")


def preview():
    imgs = [
        Image.open(OUT / "01_开场还有反方向_1080x1920.png"),
        Image.open(OUT / "02_反方向的问题_1080x1920.png"),
        Image.open(OUT / "03_主题反向隐含赔率_1080x1920.png"),
        Image.open(OUT / "04_普通隐含赔率看多赢_1080x1920.png"),
        Image.open(OUT / "05_反向隐含赔率看多输_1080x1920.png"),
    ]
    thumb_w = 360
    thumb_h = 640
    pad = 36
    label_h = 80
    canvas = Image.new("RGB", (thumb_w * 5, thumb_h + label_h), (245, 240, 230))
    dd = ImageDraw.Draw(canvas)
    for i, img in enumerate(imgs, 1):
        t = img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        canvas.paste(t, ((i - 1) * thumb_w, 0))
        draw_center(dd, ((i - 1) * thumb_w, thumb_h, i * thumb_w, thumb_h + label_h), f"{i:02d}", font(44, False), (45, 45, 45))
    canvas.save(REVIEW / "01-05_preview.png", quality=95)


def main():
    img01()
    img02()
    img03()
    img04()
    img05()
    preview()


if __name__ == "__main__":
    main()
