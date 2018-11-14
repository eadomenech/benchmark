#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import sys

import math
from PIL import Image

import numpy as np


def calc_metric(watermark, watermark_with_noise):
    return BER(watermark, watermark_with_noise)


def BER(image1, image2):
    img1 = image1.convert('L')
    img2 = image2.convert('L')
    array1 = np.asarray(img1)
    array2 = np.asarray(img2)
    S = 0
    B = array1.size
    for i in range(len(array1)):
        for j in range(len(array1[0])):
            if array1[i, j] != array2[i, j]:
                S += 1
    BER = float(S)/B
    return BER


def main(args):
    watermark_filename = None
    watermark_with_noise_filename = None

    options, remainder = getopt.getopt(
        sys.argv[1:], 'i:w:v',
        ['image', 'watermark', 'output='])

    for opt, arg in options:
        if opt in ('-i', '--image'):
            watermark_filename = arg
        elif opt in ('-w', '--watermark'):
            watermark_with_noise_filename = arg

    if watermark_filename and watermark_with_noise_filename:
        watermark = Image.open(watermark_filename)
        watermark_with_noise = Image.open(watermark_with_noise_filename)
        print(calc_metric(watermark, watermark_with_noise))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
