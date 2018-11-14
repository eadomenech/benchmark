#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import sys

import math
from PIL import Image


def calc_metric(cover_image, watermarked_image):
    return PSNR_RGB(cover_image, watermarked_image)


def PSNR_RGB(img1, img2):
    MSE = MSE_RGB(img1, img2)
    if MSE != 0:
        return 10*(math.log10(255**2/MSE))
    else:
        return 100


def MSE_RGB(img1, img2):
    w1 = img1.size[0]
    h1 = img1.size[1]
    w2 = img2.size[0]
    h2 = img2.size[1]
    if (w1 != w2) or (h1 != h2):
        return Exception
    mse = [0, 0, 0]
    MSE = 0
    pixels1 = img1.load()  # create the pixel map
    pixels2 = img2.load()
    a = []
    b = []
    for i in range(w1):    # for every pixel:
        for j in range(h1):
            b.append(abs(pixels1[i, j][0]-pixels2[i, j][0]))
            mse[0] = mse[0] + (math.fabs(pixels1[i, j][0]-pixels2[i, j][0]))**2
            mse[1] = mse[1] + (math.fabs(pixels1[i, j][1]-pixels2[i, j][1]))**2
            mse[2] = mse[2] + (math.fabs(pixels1[i, j][2]-pixels2[i, j][2]))**2
        a.append(b)
    mse = (mse[0] + mse[1] + mse[2]) / 3
    MSE = mse / (w1*h1)

    return MSE


def main(args):
    cover_filename = None
    watermarked_filename = None

    options, remainder = getopt.getopt(
        sys.argv[1:], 'i:w:v',
        ['image', 'watermarked', 'output='])

    for opt, arg in options:
        if opt in ('-i', '--image'):
            cover_filename = arg
        elif opt in ('-w', '--watermarked'):
            watermarked_filename = arg

    if cover_filename and watermarked_filename:
        cover_image = Image.open(cover_filename)
        watermarked_image = Image.open(watermarked_filename)
        print(calc_metric(cover_image, watermarked_image))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
