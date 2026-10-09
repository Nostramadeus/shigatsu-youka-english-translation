"""warn_colors.py - sample the text colour of the content-warning word pictures.

For each picture: the mean visible colour (the coordinator's metric), the CORE colour (opaque, eroded away from
the anti-aliased rim) and the RIM colour (the outermost ring of the glyph). Runs over the extracted original and
over our replacement, side by side.
"""
import os
import sys

import numpy as np
import cv2
from PIL import Image

ORIG = "work/images/gal/グラフィック/タイトル/残酷/"
NEW = "work/グラフィック/タイトル/残酷/"
PNG = "work/images/png/グラフィック/タイトル/残酷/"

WORDS = ["児童惨殺", "薬物", "触手", "死体", "カニバリズム", "殺人", "虫", "いじめ", "死姦", "監禁", "血",
         "暴力", "人体実験", "内臓", "人体欠損", "怪異", "下ネタ", "脅かし", "残酷"]


def load(path):
    if path.endswith(".png"):
        return np.array(Image.open(path).convert("RGBA"))
    import livemaker.GalImagePlugin  # noqa: F401
    im = Image.open(path)
    im.load()
    return np.array(im.convert("RGBA"))


def mode_colour(px):
    if len(px) == 0:
        return None
    q = (px // 16).astype(np.int32)
    k = np.bincount(q[:, 0] * 256 + q[:, 1] * 16 + q[:, 2]).argmax()
    sel = (q[:, 0] * 256 + q[:, 1] * 16 + q[:, 2]) == k
    return px[sel].mean(axis=0)


def stats(a):
    rgb, al = a[:, :, :3], a[:, :, 3]
    vis = (al > 0) & (rgb.astype(int).sum(axis=2) > 60)
    if vis.sum() == 0:
        return None
    mean = rgb[vis].mean(axis=0)
    solid = al > 240
    core = cv2.erode(solid.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    if core.sum() < 20:
        core = solid
    rim = solid & ~core
    return {"n": int(vis.sum()), "mean": mean, "core": mode_colour(rgb[core]) if core.sum() else None,
            "rim": mode_colour(rgb[rim]) if rim.sum() > 20 else None,
            "corepx": int(core.sum()), "rimpx": int(rim.sum())}


def fmt(c):
    return "-" if c is None else "%3d,%3d,%3d" % (c[0], c[1], c[2])


def hexc(c):
    return "#%02x%02x%02x" % (int(round(c[0])), int(round(c[1])), int(round(c[2])))


print("%-12s | %-26s | %-26s | hex(core)" % ("word", "ORIGINAL mean / core / rim", "OURS mean / core / rim"))
for w in WORDS:
    o = stats(load(ORIG + w + ".gal"))
    p = NEW + w + ".gal"
    n = stats(load(p)) if os.path.exists(p) else None
    print("%-12s | %s %s %s | %s | %s" % (
        w, fmt(o["mean"]), fmt(o["core"]), fmt(o["rim"]),
        ("%s %s %s" % (fmt(n["mean"]), fmt(n["core"]), fmt(n["rim"]))) if n else "NOT SHIPPED",
        hexc(o["core"]) + (" rim " + hexc(o["rim"]) if o["rim"] is not None else " rim -")))


# --- the composite: sample only the lettering (red / pink pixels), not the black plate -------------------
def word_colour(a, label):
    rgb = a[:, :, :3].astype(int)
    red = rgb[:, :, 0] - np.maximum(rgb[:, :, 1], rgb[:, :, 2])
    m = red > 60
    core = cv2.erode(m.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    rim = m & ~core
    print("%-28s lettering px=%d  mean=%s  core=%s  rim=%s" % (
        label, int(m.sum()), fmt(rgb[m].mean(axis=0)), fmt(mode_colour(rgb[core])) if core.sum() else "-",
        fmt(mode_colour(rgb[rim])) if rim.sum() > 20 else "-"))
    pink = (rgb[:, :, 0] > 150) & (rgb[:, :, 2] > 120) & (rgb[:, :, 1] < 200) & (rgb[:, :, 0] > rgb[:, :, 1] + 30)
    pink = pink & ~m
    if pink.sum() > 50:
        print("%-28s pink px=%d mode=%s" % ("", int(pink.sum()), fmt(mode_colour(rgb[pink]))))


print()
word_colour(load(ORIG + "残酷.gal"), "composite ORIGINAL")
word_colour(load(NEW + "残酷.gal"), "composite OURS")
