# Coded by Berna Bas
# 8.10.2019
# This code blurs marked characters with #. It is coded for a psychological research. You can use the code or customize.


from PIL import Image, ImageColor, ImageFont, ImageDraw
import codecs
import cv2
import numpy as np
import sys
import os
import datetime

FONT_SIZE = 18
IMG_SIZE = [1200, 900]  # WIDTH HEIGHT


# convert string to image
def generate_image(str):
    text = Image.new("RGBA", IMG_SIZE, ImageColor.getrgb("rgb(255,255,255)"))
    fnt = ImageFont.truetype(font="fonts/consola.ttf", size=FONT_SIZE)
    img = ImageDraw.Draw(text)
    # img.text((0, 0), str, font=fnt, fill=(0, 0, 0))
    img.multiline_text((10, 10), str, fill=(0, 0, 0), font=fnt, spacing=10)
    text.save("out.png", "PNG", dpi=(600, 600))
    return text


# blur given image
def blur(img):
    kernel = np.ones((4, 4), np.float) / 15
    return cv2.filter2D(img, -1, kernel)


# find characters to be blurred
def getBlurPoints(text):
    row = 0
    column = 0
    points = []  # location of marked ch

    for i, c in enumerate(text):

        # found marked character
        if c == '#':
            points.append([row, column])
        else:
            column += 1

        if c == '\n':
            row += 1
            column = 0

    return points


# blur parts on the image by coordinates
def blurRegions(img, points):
    if not points:
        return

    size = [FONT_SIZE + 6, int(FONT_SIZE * 0.6)]  # y x

    row_height = size[0]
    col_width = size[1]
    space = 10
    line_space = int(IMG_SIZE[1] / (FONT_SIZE * 2)) - FONT_SIZE - 3  # it is adjusted for 18 pixel size

    for row, col in points:

        if row > 0:
            space = line_space

        pixel_y = row * row_height + space
        pixel_x = col * col_width + 10
        cropped_img = img[pixel_y:pixel_y + size[0], pixel_x:pixel_x + size[1]]
        blurred_img = blur(cropped_img)
        img[pixel_y:pixel_y + size[0], pixel_x:pixel_x + size[1]] = blurred_img

    return img


def main(args):
    print(args)
    if len(args) != 4:
        print("arguments should be text_file width height")
        return

    if not os.path.isfile(args[1]):
        print("text file is not found")
        return
    print("Working...")

    # assign arguments
    IMG_SIZE[0] = int(args[2])
    IMG_SIZE[1] = int(args[3])

    # read text file
    file = codecs.open(args[1], mode="r", encoding="utf-8")
    text = file.read()
    file.close()

    # get points to be blurred
    points = getBlurPoints(text)

    # clear signs
    text = text.replace("#", "")

    # text to image
    img = generate_image(text)

    # convert image to array in order to use image in opencv
    opencv_image = np.array(img)

    # blur given points
    img = blurRegions(opencv_image, points)

    print("{} characters are blurred.".format(len(points)))

    # plt.xticks(range(0, 50))
    # plt.yticks(range(0, 50))
    # plt.imshow(opencv_image)
    # plt.show()
    now = datetime.datetime.now()
    out_file = now.strftime("%Y%m%d %H%M%S") + "-blurred.png"
    cv2.imwrite(out_file, img)

    print("Image is created.")
    print("Bye.")


args = sys.argv
# run the app
main(args)
