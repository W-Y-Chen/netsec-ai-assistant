"""
创建网安 AI 助手专属图标
设计：黑客帝国风格 - 黑色背景 + 绿色 + 盾牌 + 终端
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# 创建 256x256 大图（满足系统图标要求）
SIZE = 256
img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 1. 圆角矩形背景（深蓝黑色）
def rounded_rectangle(draw, xy, radius, fill):
    """画圆角矩形"""
    x1, y1, x2, y2 = xy
    # 填充矩形
    draw.rectangle([x1 + radius, y1, x2 - radius, y1 + radius], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.rectangle([x1 + radius, y2 - radius, x2 - radius, y2], fill=fill)
    # 填充四角
    draw.pieslice([x1, y1, x1 + 2*radius, y1 + 2*radius], 180, 270, fill=fill)
    draw.pieslice([x2 - 2*radius, y1, x2, y1 + 2*radius], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - 2*radius, x1 + 2*radius, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - 2*radius, y2 - 2*radius, x2, y2], 0, 90, fill=fill)

# 外层深色圆角矩形
rounded_rectangle(draw, [10, 10, 246, 246], 30, fill=(10, 20, 35, 255))

# 内层边框（终端绿色）
def draw_terminal_border(draw, x, y, w, h, color, width=3):
    """画终端风格的边框"""
    # 上边
    draw.line([x, y, x+w, y], fill=color, width=width)
    # 下边
    draw.line([x, y+h, x+w, y+h], fill=color, width=width)
    # 左边
    draw.line([x, y, x, y+h], fill=color, width=width)
    # 右边
    draw.line([x+w, y, x+w, y+h], fill=color, width=width)

# 2. 终端窗口框架
draw_terminal_border(draw, 30, 50, 196, 180, (0, 255, 130, 255))

# 3. 顶部红黄绿按钮（终端风格）
button_y = 38
draw.ellipse([36, button_y, 50, button_y+14], fill=(255, 95, 86, 255))
draw.ellipse([56, button_y, 70, button_y+14], fill=(255, 189, 46, 255))
draw.ellipse([76, button_y, 90, button_y+14], fill=(39, 201, 63, 255))

# 标题栏
draw.line([30, 58, 226, 58], fill=(0, 255, 130, 255), width=1)

# 4. 代码雨效果（垂直绿线）
import random
random.seed(42)
for i in range(15):
    x = 40 + i * 13
    drop_height = random.randint(15, 40)
    drop_y = 75 + random.randint(0, 30)
    # 渐变绿色
    for j in range(drop_height):
        alpha = int(255 * (1 - j / drop_height))
        color = (0, 255, 130, alpha)
        draw.line([x, drop_y + j * 3, x, drop_y + (j + 1) * 3], fill=color, width=1)

# 5. 中央盾牌设计
shield_x = 128
shield_y = 145
# 盾牌轮廓（终端绿）
shield_points = [
    (shield_x - 30, shield_y - 35),
    (shield_x + 30, shield_y - 35),
    (shield_x + 30, shield_y - 5),
    (shield_x, shield_y + 35),
    (shield_x - 30, shield_y - 5),
]
draw.polygon(shield_points, fill=(0, 80, 40, 255), outline=(0, 255, 130, 255))

# 盾牌内边框
inner_points = [
    (shield_x - 22, shield_y - 28),
    (shield_x + 22, shield_y - 28),
    (shield_x + 22, shield_y - 7),
    (shield_x, shield_y + 25),
    (shield_x - 22, shield_y - 7),
]
draw.polygon(inner_points, outline=(0, 255, 130, 255))

# 盾牌中心 - 大写 AI 字母
try:
    font_large = ImageFont.truetype("consola.ttf", 30)
    font_path = "consola.ttf"
except:
    try:
        font_large = ImageFont.truetype("arial.ttf", 30)
    except:
        font_large = ImageFont.load_default()

# AI 文字
text = "AI"
bbox = draw.textbbox((0, 0), text, font=font_large)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]
draw.text((shield_x - text_w/2 - 2, shield_y - 18), text, fill=(0, 255, 130, 255), font=font_large)

# 6. 底部装饰 - "NETSEC" 字样
try:
    font_small = ImageFont.truetype("consola.ttf", 14)
except:
    font_small = ImageFont.load_default()

netsec_text = "NETSEC"
bbox = draw.textbbox((0, 0), netsec_text, font=font_small)
text_w = bbox[2] - bbox[0]
draw.text((shield_x - text_w/2 - 1, 215), netsec_text, fill=(0, 255, 130, 255), font=font_small)

# 7. 角落装饰 - 提示符 ">"
prompt1 = ">"
draw.text((40, 78), prompt1, fill=(0, 255, 130, 255), font=font_small)
prompt2 = ">"
draw.text((40, 98), prompt2, fill=(0, 255, 130, 255), font=font_small)
prompt3 = ">"
draw.text((40, 118), prompt3, fill=(0, 255, 130, 255), font=font_small)

# 保存图标
output_path = r"E:\网安\AI助手代码\netsec_ai_icon.ico"

# 先保存 PNG 多尺寸
img.save(r"E:\网安\AI助手代码\netsec_ai_icon.png")

# 保存 ICO（多种尺寸）
img.save(output_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])

print(f"✅ 图标已创建: {output_path}")
print(f"   PNG 预览: E:\\网安\\AI助手代码\\netsec_ai_icon.png")
print(f"   ICO 多尺寸: 256/128/64/48/32/16")
