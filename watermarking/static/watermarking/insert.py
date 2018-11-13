#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import sys

from PIL import Image


def insert(cover_image, watermark_image):
    return cover_image


def main(args):
    input_filename = None
    watermark_filename = None
    output_filename = None

    # print('ARGV      :', sys.argv[1:])

    options, remainder = getopt.getopt(
        sys.argv[1:], 'i:w:o:v',
        ['input', 'watermark', 'output='])
    # print('OPTIONS   :', options)

    for opt, arg in options:
        if opt in ('-i', '--input'):
            input_filename = arg
        elif opt in ('-w', '--watermark'):
            watermark_filename = arg
        elif opt in ('-o', '--output'):
            output_filename = arg

    if input_filename and watermark_filename:
        cover_image = Image.open(input_filename)
        watermark_image = Image.open(watermark_filename)
        watermarked_image = insert(cover_image, watermark_image)
        watermarked_image.save(output_filename, quality='keep')

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
