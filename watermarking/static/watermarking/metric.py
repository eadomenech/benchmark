#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import sys

from PIL import Image


def calc_metric(cover_image, watermarked_image):
    if cover_image.size != watermarked_image.size:
        return -2
    return 100


def main(args):
    cover_filename = None
    watermarked_filename = None

    # print('ARGV      :', sys.argv[1:])

    options, remainder = getopt.getopt(
        sys.argv[1:], 'i:w:v',
        ['image', 'watermarked', 'output='])
    # print('OPTIONS   :', options)

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
