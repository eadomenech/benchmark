#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import sys

from PIL import Image
import numpy as np
from transforms.DqKT import DqKT
# from transforms_gpgpu.dqkt_gpgpu import DqktGPGPU
from transforms.DAT import DAT
from block_tools.BlockTools import BlockTools
from qr_tools.MyQR62 import MyQR62

from scipy import misc
import math


def binary2int(binary):
    # Devuelve el entero correspondiente a una lista de binarios
    n = len(binary)
    v = 0
    for i in range(n):
        v += (2**(n-i-1))*binary[i]
    return v


def get_dwt(chromosome):
    """
    Devuelve la subbanda de la DWT a utilizar (0, 1, 2, 3) -> (LL, LH, HL, HH)
    """
    return binary2int(chromosome[0:2])


def zigzag(n):
    indexorder = sorted(
        ((x, y) for x in range(n) for y in range(n)), key=lambda s: (s[0]+s[1], -s[1] if (s[0]+s[1]) % 2 else s[1]))
    return {index: n for n, index in enumerate(indexorder)}


def get_indice(m):
    zarray = zigzag(8)
    indice = []
    n = int(len(zarray) ** 0.5 + 0.5)
    for x in range(n):
        for y in range(n):
                if zarray[(x, y)] == m:
                    indice.append(x)
                    indice.append(y)
    return indice


def mypwlcm(dic, valores):
    '''
    dic: diccionario compuesto por la semila y el valor de p
    valores: lista de valores a tratar
    '''
    valores_finales = []
    cantidad_valores = len(valores)
    posiciones = orden(dic, cantidad_valores)
    # print 'Posiciones: ', posiciones
    posiciones_distintas = lista_valores_distintos(posiciones)
    # print 'Posiciones distintas: ', posiciones_distintas
    if len(posiciones_distintas) == len(posiciones):
        v = []
        for i in range(len(posiciones_distintas)):
            v.append(valores[i])
        return v
    if len(posiciones_distintas) == 1:
        return valores
    for i in range(len(posiciones_distintas)):
        valores_finales.append(valores[posiciones_distintas[i]])
    posiciones_faltantes = lista_valores_faltantes(
        posiciones_distintas, cantidad_valores)
    # print 'Faltantes: ', posiciones_faltantes
    if len(posiciones_faltantes) > 0:
        v = []
        for i in range(len(posiciones_faltantes)):
            v.append(valores[posiciones_faltantes[i]])
        valores_finales.extend(mypwlcm(dic, v))
    return valores_finales


def pwlcm(dic):
    # dic: diccionario compuesto por la semila y el valor de p
    if (dic['semilla'] >= 0) and (dic['semilla'] < dic['p']):
        x = dic['semilla'] / dic['p']
    elif (dic['semilla'] >= dic['p']) and (dic['semilla'] < 0.5):
        x = (dic['semilla'] - dic['p']) / (0.5 - dic['p'])
    elif (dic['semilla'] >= 0.5) and (dic['semilla'] < 1):
        dic['semilla'] = 1 - dic['semilla']
        x = pwlcm(dic)
    return x


def orden(dic, cant=40):
    lista = []
    for i in range(cant):
        if i != 0:
            dic_a = {}
            dic_a['semilla'] = temp
            dic_a['p'] = dic['p']
            temp = pwlcm(dic_a)
        else:
            temp = pwlcm(dic)
        lista.append(int(math.floor(math.fmod(temp * 10**14, cant))))
    return lista


def lista_valores_distintos(lista):
    lista_nueva = []
    for i in lista:
        if i not in lista_nueva:
            lista_nueva.append(i)
    return lista_nueva


def lista_valores_faltantes(posiciones_distintas, cantidad_valores):
    posiciones_faltantes = []
    for i in range(cantidad_valores):
        if i not in posiciones_distintas:
            posiciones_faltantes.append(i)
    return posiciones_faltantes


def mypwlcm_limit(dic, valores, limite):
    '''
    dic: diccionario compuesto por la semila y el valor de p
    valores: lista de valores a tratar
    '''
    valores_finales = []
    cantidad_valores = len(valores)
    posiciones = orden(dic, cantidad_valores)
    # print 'Posiciones: ', posiciones
    posiciones_distintas = lista_valores_distintos(posiciones)
    # print 'Posiciones distintas: ', posiciones_distintas
    if len(valores_finales) > limite:
        return valores_finales
    if len(posiciones_distintas) == len(posiciones):
        v = []
        for i in range(len(posiciones_distintas)):
            v.append(valores[i])
        return v
    if len(posiciones_distintas) == 1:
        return valores
    for i in range(len(posiciones_distintas)):
        valores_finales.append(valores[posiciones_distintas[i]])
    posiciones_faltantes = lista_valores_faltantes(
        posiciones_distintas, cantidad_valores)
    # print 'Faltantes: ', posiciones_faltantes
    if len(posiciones_faltantes) > 0:
        v = []
        for i in range(len(posiciones_faltantes)):
            v.append(valores[posiciones_faltantes[i]])
        valores_finales.extend(mypwlcm_limit(dic, v, limite))
    return valores_finales


def extract(watermarked_filename):
    delta = 128
    c = [1, 19]
    from image_tools.ImageTools import ImageTools
    dqkt = DqKT()
    myqr = MyQR62()
    dat = DAT()
    itools = ImageTools()

    watermarked_image = Image.open(watermarked_filename)
    watermarked_ycbcr_image = itools.rgb2ycbcr(watermarked_image)
    watermarked_array = watermarked_ycbcr_image[:, :, 0]
    bt_of_watermarked_image_without_noise = BlockTools(watermarked_array)

    extract = []

    len_of_watermark = 3844

    # Utilizar Bloques segun key
    dic = {'semilla': 0.00325687, 'p': 0.22415897}
    valores = []
    cantidad = bt_of_watermarked_image_without_noise.max_blocks()
    for i in range(cantidad):
        valores.append(i)
    v = mypwlcm_limit(dic, valores, len_of_watermark)

    for i in range(len_of_watermark):

        dqkt_block = dqkt.dqkt2(
            np.array(
                bt_of_watermarked_image_without_noise.get_block(v[i]+1),
                dtype=np.float32))

        negative = False
        if dqkt_block[get_indice(c[1])[0], get_indice(c[1])[1]] < 0:
            negative = True

        C1 = (2*delta*round(abs(dqkt_block[get_indice(c[1])[0], get_indice(c[1])[1]])/(2.0*delta)) + delta/2.0) - abs(dqkt_block[get_indice(c[1])[0], get_indice(c[1])[1]])
        C0 = (2*delta*round(abs(dqkt_block[get_indice(c[1])[0], get_indice(c[1])[1]])/(2.0*delta)) - delta/2.0) - abs(dqkt_block[get_indice(c[1])[0], get_indice(c[1])[1]])

        if negative:
            C1 *= -1
            C0 *= -1
        if C0 < C1:
            extract.append(0)
        else:
            extract.append(1)

    wh = int(math.sqrt(len_of_watermark))
    extract_image = Image.new("1", (wh, wh), 255)
    array_extract_image = misc.fromimage(extract_image)

    for i in range(wh):
        for y in range(wh):
            if extract[wh*i+y] == 0:
                array_extract_image[i, y] = 0

    watermark_array_image = misc.toimage(array_extract_image)
    for i in range(10):
        watermark_array_image = dat.dat2(watermark_array_image)
    array = misc.fromimage(watermark_array_image)
    return misc.toimage(myqr.get_resconstructed(array))


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

    if input_filename:
        extract_watermark = extract(input_filename)
        extract_watermark.save(output_filename, quality=100)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
