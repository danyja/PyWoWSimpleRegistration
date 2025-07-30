import base64
import io
import random
import string

from PIL import Image, ImageDraw, ImageFilter, ImageFont


def generate_captcha(width=130, height=50, length=6,
                     font_size=30, font_path=None,
                     line_count=5, dot_count=50):
    """
    生成带干扰的验证码图片

    参数:
        width: 图片宽度
        height: 图片高度
        length: 验证码长度
        font_size: 字体大小
        font_path: 字体路径(如果为None则使用默认字体)
        line_count: 干扰线数量
        dot_count: 干扰点数量

    返回:
        (image, captcha_text) 元组
    """
    # 创建空白图片
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 生成随机验证码文本
    chars = string.ascii_letters + string.digits
    captcha_text = ''.join(random.choice(chars) for _ in range(length))

    # 加载字体
    if not font_path:
        font_path = "c:\\windows\\fonts\\msyh.ttf"
    font = ImageFont.truetype(font_path, font_size)
    # 计算文本位置(居中)
    bbox = font.getbbox(captcha_text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) / 2
    y = (height - text_height) / 2

    # 绘制验证码文本(每个字符随机颜色和位置)
    for i, char in enumerate(captcha_text):
        # 随机颜色(避免太浅的颜色)
        text_color = (
            random.randint(50, 200),
            random.randint(50, 200),
            random.randint(50, 200)
        )

        # 稍微随机偏移每个字符的位置
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)

        # 计算单个字符的宽度
        char_bbox = font.getbbox(char)
        char_width = char_bbox[2] - char_bbox[0]

        draw.text((x + offset_x, y + offset_y),
                  char, font=font, fill=text_color)
        x += char_width  # 移动到下一个字符的位置

    # 添加干扰线
    for _ in range(line_count):
        line_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        start = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([start, end], fill=line_color, width=random.randint(1, 2))

    # 添加干扰点
    for _ in range(dot_count):
        dot_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        position = (random.randint(0, width), random.randint(0, height))
        draw.point(position, fill=dot_color)

    image = image.filter(ImageFilter.SMOOTH)

    # 添加边框
    draw.rectangle([0, 0, width-1, height-1], outline=(150, 150, 150))

    # 转成base64格式
    buf = io.BytesIO()
    image.save(buf, "png")
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return img_base64, captcha_text


# 示例使用
if __name__ == "__main__":
    # 生成验证码
    image, captcha_text = generate_captcha(
        width=120,
        height=50,
        length=6,
    )

    # 保存验证码图片
    # image.save("captcha.png", "PNG")
    print(f"验证码已生成: {captcha_text}")
