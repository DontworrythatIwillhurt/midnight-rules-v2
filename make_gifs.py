# -*- coding: utf-8 -*-
"""将午夜规则的静态 PNG 资产合成为循环 GIF 帧动画。"""
import math
import os
import random

from PIL import Image, ImageEnhance

random.seed(44)

SRC = r"C:\Users\19264\.gemini\antigravity\scratch\midnight-rules"
W = 560  # 输出宽度，控制文件体积


def load(name):
    im = Image.open(os.path.join(SRC, name)).convert("RGB")
    ratio = W / im.width
    return im.resize((W, int(im.height * ratio)), Image.LANCZOS)


def save_gif(frames, name, duration=110):
    frames = [f.convert("P", palette=Image.ADAPTIVE, colors=48, dither=Image.FLOYDSTEINBERG) for f in frames]
    out = os.path.join(SRC, name)
    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=duration, loop=0, optimize=True, disposal=2)
    print(f"{name}: {os.path.getsize(out)//1024} KB, {len(frames)} 帧")


def red_figure_anim():
    """红衣人：呼吸般上下浮动 + 明暗搏动。"""
    im = load("red_figure.png")
    Wd, Ht = im.size
    amp = 6
    frames = []
    for i in range(14):
        t = i / 14 * 2 * math.pi
        dy = int(amp * math.sin(t))
        bright = 0.82 + 0.2 * (0.5 + 0.5 * math.sin(t + 1.2))
        canvas = Image.new("RGB", (Wd, Ht + 2 * amp), (2, 2, 2))
        canvas.paste(ImageEnhance.Brightness(im).enhance(bright), (0, amp + dy))
        frames.append(canvas)
    save_gif(frames, "red_figure_anim.gif", 120)


def entity_glitch():
    """不可名状实体：RGB 通道错位 + 横条撕裂 + 频闪。"""
    im = load("unspeakable_entity.png")
    Wd, Ht = im.size
    frames = []
    for i in range(10):
        f = im.copy()
        if i % 3 != 0:
            r, g, b = f.split()
            dx = random.randint(-9, 9)
            r = r.transform((Wd, Ht), Image.AFFINE, (1, 0, dx, 0, 1, 0))
            b = b.transform((Wd, Ht), Image.AFFINE, (1, 0, -dx, 0, 1, 0))
            f = Image.merge("RGB", (r, g, b))
        if i % 4 == 1:
            y = random.randint(0, Ht - 50)
            h = random.randint(12, 42)
            dx = random.choice([-1, 1]) * random.randint(14, 48)
            band = f.crop((0, y, Wd, y + h))
            f.paste(band, (dx, y))
        f = ImageEnhance.Brightness(f).enhance(random.uniform(0.6, 0.95))
        frames.append(f)
    save_gif(frames, "entity_glitch.gif", 90)


def window_hands_anim():
    """鬼手拍窗：画面抖动 + 每四帧一次黑闪。"""
    im = load("scratching_window.png")
    Wd, Ht = im.size
    frames = []
    for i in range(12):
        dx = random.randint(-5, 5)
        dy = random.randint(-4, 4)
        canvas = Image.new("RGB", (Wd, Ht), (0, 0, 0))
        canvas.paste(im, (dx, dy))
        bright = 0.55 if i % 4 == 3 else random.uniform(0.85, 1.0)
        frames.append(ImageEnhance.Brightness(canvas).enhance(bright))
    save_gif(frames, "window_hands_anim.gif", 100)


def seller_anim():
    """乘务员推车：缓慢的尸斑式明暗脉动。"""
    im = load("seller_bg.png")
    frames = []
    for i in range(12):
        t = i / 12 * 2 * math.pi
        bright = 0.78 + 0.24 * (0.5 + 0.5 * math.sin(t))
        frames.append(ImageEnhance.Brightness(im).enhance(bright))
    save_gif(frames, "seller_anim.gif", 130)


def subway_anim():
    """空车厢：灯管电压不稳式微闪。"""
    im = load("subway_bg.png")
    frames = []
    for i in range(10):
        if i in (3, 7):
            bright = 0.72
        else:
            bright = random.uniform(0.92, 1.0)
        frames.append(ImageEnhance.Brightness(im).enhance(bright))
    save_gif(frames, "subway_anim.gif", 140)


if __name__ == "__main__":
    red_figure_anim()
    entity_glitch()
    window_hands_anim()
    seller_anim()
    subway_anim()
    print("全部 GIF 生成完成")
