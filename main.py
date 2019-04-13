#!/usr/bin/env python3
"""
File: main.py
Authors:    Martin Kopec <xkopec42@gmail.com>
            Martin Krajnak <krajnakmatto@gmail.com>
            Patrik Segedy <patriksegedy@gmail.com>
            Tibor Dudlak <tibor.dudlak@gmail.com>
"""

import argparse
import os
import random
import requests

from video import Video

# arg keys
PRODUCT = "product"
EFFECT = "effect"
BACKGROUND = "background"
TEXT = "text"
ANIMATION = "animation"
FONT = "font"
STICKER = "sticker"
PLATFORM = "platform"
SPEED = "speed"
MULTI = "multi"
TITLE = "title"
PRICE = "price"
RENDER = "render"
LINE = "line"
OUTPUT = "output"


# used for csv data
PRODUCT_NAME = 1
PRODUCT_IMAGE = 3
PRODUCT_PRICE = 4
PRODUCT_IMAGES = 10
PRODUCT_SIZES = -1


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--background",
        default="data/videos/4KRGBcolors.mp4",
        required=False,
        help="Background",
    )
    parser.add_argument(
        "-a",
        "--animation",
        default="curve4",
        required=False,
        help="Animation",
    )
    parser.add_argument(
        "-f",
        "--font",
        default="data/fonts/Dogfish/Dogfish.ttf",
        required=False,
        help="Font to use",
    )
    parser.add_argument(
        "-e",
        "--effect",
        default="green",
        required=False,
        help="Color effect to use",
    )
    parser.add_argument(
        "-s",
        "--speed",
        default=6,
        type=int,
        required=False,
        help="Speed of the animation (pixels per frame)",
    )
    parser.add_argument(
        "-m",
        "--multi",
        default=False,
        type=bool,
        required=False,
        help="Multiple product images on video frame.",
    )
    parser.add_argument(
        "-t",
        "--title",
        default=1,
        type=int,
        required=False,
        help="Show title text.",
    )
    parser.add_argument(
        "-p",
        "--price",
        default=1,
        type=int,
        required=False,
        help="Show price tag.",
    )
    parser.add_argument(
        "-r",
        "--render",
        default=False,
        action="store_true",
        required=False,
        help="Show realtime rendering.",
    )
    parser.add_argument(
        "-l",
        "--line",
        default=None,
        type=int,
        required=False,
        help="Line from csv.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.mp4",
        type=str,
        required=False,
        help="Output file.",
    )

    return parser.parse_args()


def get_random_line(csvfile="data/feeds/Footshop feed.csv", line=None):
    lines = []
    with open(csvfile) as f:
        lines = [line for line in f]
        filesize = len(lines)

    offset = random.randrange(2, filesize)  # first 2 lines are comments

    return lines[offset if not line else line+2]


def get_image(url):
    r = requests.get(url)
    if not r.status_code == 200:
        raise ValueError
    img_name = url.split("=")[-1]+".png"
    with open(img_name, "wb") as f:
        f.write(r.content)
    return img_name


if __name__ == "__main__":
    args = vars(parse_args())
    print("Hello ROIHUNTER!\n")
    for key in args.keys():
        print(key, ":", args[key])

    downloaded = []
    while not downloaded:
        data = get_random_line(line=args[LINE]).split("\t")
        images = data[PRODUCT_IMAGES].split(",") + \
            [data[PRODUCT_IMAGE].strip('"')]
        for image in images:
            try:
                downloaded += [get_image(image.strip('"'))]
            except ValueError:
                continue

    if args[MULTI]:
        downloaded = ["data/sale/doge.png", "data/sale/kod.png"] + downloaded
        print(downloaded)

    title = data[PRODUCT_NAME].replace('"', "")

    ad = Video(
        video_file=args[BACKGROUND],
        image_paths=downloaded,
        title=title if args[TITLE] else "",
        text=data[PRODUCT_PRICE].strip('"') if args[PRICE] else "",
        text_speed=60,
        font=args[FONT],
        color_effect=args[EFFECT],
        animation=args[ANIMATION],
        speed=args[SPEED],
        multi=args[MULTI],
        render=args[RENDER],
        output=args[OUTPUT]
    )

    ad.play()
    for tmp_image in downloaded:
        if tmp_image not in ["data/sale/doge.png", "data/sale/kod.png"]:
            os.remove(tmp_image)
