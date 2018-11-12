#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import sys

from PIL import Image


def noising(image):
    return image


def main(args):
    input_filename = None
    output_filename = None

    # print('ARGV      :', sys.argv[1:])

    options, remainder = getopt.getopt(
        sys.argv[1:], 'i:o:v',
        ['input', 'output='])
    # print('OPTIONS   :', options)

    for opt, arg in options:
        if opt in ('-i', '--input'):
            input_filename = arg
        elif opt in ('-o', '--output'):
            output_filename = arg

    print('INPUT    :', input_filename)
    print('OUTPUT    :', output_filename)
    print('REMAINING :', remainder)

    if input_filename and output_filename:
        image = Image.open(input_filename)
        image_with_noise = noising(image)
        image_with_noise.save(output_filename)
    else:
        print('input_filename or output_filename are None')

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
