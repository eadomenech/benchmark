#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import sys

from PIL import Image


def extract(watermarked_image):
    return watermarked_image


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

    print('INPUT    :', input_filename)
    print('WATERMARK    :', watermark_filename)
    print('OUTPUT    :', output_filename)
    print('REMAINING :', remainder)

    if input_filename:
        watermarked_image = Image.open(input_filename)
        watermark_image = Image.open(watermark_filename)
        extract_watermark = extract(watermark_image)
        extract_watermark.save(output_filename, quality='keep')

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
