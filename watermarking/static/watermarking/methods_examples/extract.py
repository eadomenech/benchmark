#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import sys

import math
from PIL import Image
import numpy as np
from scipy import misc


def orth_matrix(x):
    if x == 13:
        # Dual Hahn discrete orthogonal polynomial
        return np.array([
            [0.353553, -0.353553, 0.353553, -0.353553, 0.353553, -0.353553,
                0.353553, -0.353553],
            [0.540062, -0.385758, 0.231455, -0.0771517, -0.0771517, 0.231455,
                -0.385758, 0.540062],
            [0.540062, -0.0771517, -0.231455, 0.385758, -0.385758, 0.231455,
                0.0771517, -0.540062],
            [0.43082, 0.307729, -0.43082, 0.184637, 0.184637, -0.43082,
                0.307729, 0.43082],
            [0.282038, 0.523785, -0.120873, -0.36262, 0.36262, 0.120873,
                -0.523785, -0.282038],
            [0.149786, 0.492155, 0.363766, -0.32097, -0.32097, 0.363766,
                0.492155, 0.149786],
            [0.0615457, 0.307729, 0.553912, 0.307729, -0.307729, -0.553912,
                -0.307729, -0.0615457],
            [0.0170697, 0.119488, 0.358464, 0.59744, 0.59744, 0.358464,
                0.119488, 0.0170697]])
    if x == 14:
        # Racah discrete orthogonal polynomial
        return np.array([
            [0.125, -0.216506, 0.279508, -0.330719, 0.375, -0.414578,
                0.450694, -0.484123],
            [0.216506, -0.35119, 0.391909, -0.354604, 0.237126, -0.0341938,
                -0.260208, 0.652186],
            [0.279508, -0.391909, 0.291667, -0.0352148, -0.279508, 0.485584,
                -0.335927, -0.505181],
            [0.330719, -0.354604, 0.0352148, 0.352273, -0.4338, -0.0142451,
                0.614279, 0.271699],
            [0.375, -0.237126, -0.279508, 0.4338, 0.125, -0.554566, -0.450694,
                -0.102693],
            [0.414578, -0.0341938, -0.485584, -0.0142451, 0.554566, 0.498626,
                0.18467, 0.0261995],
            [0.450694, 0.260208, -0.335927, -0.614279, -0.450694, -0.18467,
                -0.0416667, -0.00406883],
            [0.484123, 0.652186, 0.505181, 0.271699, 0.102693, 0.0261995,
                0.00406883, 0.000291375]])


def multiply_matrix(A, B, C):
    if C == []:
        return np.dot(A, B)
    else:
        return np.dot(np.dot(A, B), C)


# This class calculte the discrete orthogonal moments
class Dtop:

    def __init__(self, x, y):
        self.row = x
        self.col = y

    def dtop2(self, A):
        P = orth_matrix(self.row)
        Q = orth_matrix(self.col)
        return multiply_matrix(P.T, A, Q)

    def idtop2(self, A):
        P = orth_matrix(self.row)
        Q = orth_matrix(self.col)
        matrix = multiply_matrix(P, A, Q.T)
        # Fix overflow and underflow problem
        for i in range(8):
            for j in range(8):
                if (matrix[i, j] - int(matrix[i, j])) < 0.5:
                    matrix[i, j] = int(matrix[i, j])
                else:
                    matrix[i, j] = int(matrix[i, j]) + 1
                if matrix[i, j] > 255:
                    matrix[i, j] = 255.0
                elif matrix[i, j] < 0:
                    matrix[i, j] = 0.0
        return matrix


class BlocksImage():
    def __init__(self, image_plane, sblock_rows=8, sblock_cols=8):
        self.matrix = image_plane
        self.size_block_rows = sblock_rows
        self.size_block_cols = sblock_cols
        self.blocks_in_rows = len(image_plane) // self.size_block_rows
        self.blocks_in_cols = len(image_plane[1]) // self.size_block_cols

    def get(self):
        return self.matrix

    def max_num_blocks(self):
        return self.blocks_in_rows * self.blocks_in_cols

    def image_size(self):
        return self.matrix.shape

    def get_coord(self, num_block):
        if num_block < self.max_num_blocks():
            L = []
            row_block = int(num_block / self.blocks_in_cols)
            col_block = num_block % self.blocks_in_cols
            L.append(row_block * self.size_block_rows)
            L.append((row_block + 1) * self.size_block_rows)
            L.append(col_block * self.size_block_cols)
            L.append((col_block + 1) * self.size_block_cols)
            return L
        raise Exception("There is no such block")

    def get_block(self, num_block):
        try:
            pos = self.get_coord(num_block)
            return self.matrix[pos[0]:pos[1], pos[2]:pos[3]]
        except Exception:
            return None

    def set_block(self, block, num_block):
        pos = self.get_coord(num_block)
        self.matrix[pos[0]:pos[1], pos[2]:pos[3]] = block


def div_key(key):
    cad_1 = ""
    cad_2 = ""
    for i in range(len(key)):
        if i % 2 == 0:
            cad_1 += key[i]
        else:
            cad_2 += key[i]
    return [cad_1, cad_2]


def char2dec(mens):
    L = []
    for i in range(len(mens)):
        L.append(ord(mens[i]))
    return L


def char2bin(mens):
    cad = ""
    L = char2dec(mens)
    for i in range(len(L)):
        cad += np.binary_repr(L[i], width=8)
    return cad


def sha512_bin(key):
    import hashlib
    return char2bin(hashlib.sha512(key.encode('utf-8')).hexdigest())


def matrix2vector(A):
    L = []
    for i in range(len(A)):
        L.extend(A[i, :])
    return L


def matrix_zig_zag():
    A = np.array([
        [0,     1,     8,    16,     9,     2,     3,    10],
        [17,    24,    32,    25,    18,    11,     4,     5],
        [12,    19,    26,    33,    40,    48,    41,    34],
        [27,    20,    13,     6,     7,    14,    21,    28],
        [35,    42,    49,    56,    57,    50,    43,    36],
        [29,    22,    15,    23,    30,    37,    44,    51],
        [58,    59,    52,    45,    38,    31,    39,    46],
        [53,    60,    61,    54,    47,    55,    62,    63]])
    return A


def vzig_zag_scan(A):
    L = []
    pos = matrix2vector(matrix_zig_zag())
    seq = matrix2vector(A)
    for i in range(len(pos)):
        L.append(seq[pos[i]])
    return L


def increase_string(seq, n):
    cad = ""
    while len(cad) < n:
        cad += seq
    return cad[:n]


def pwlcm(x, p):
    if x >= 0 and x < p:
        return x / p
    elif x >= p and x < 0.5:
        return (x - p) / (0.5 - p)
    elif x >= 0.5 and x < 1:
        return pwlcm(1 - x, p)


def chaotic_map(x, p, n):
    L = []
    for i in range(n):
        x = pwlcm(x, p)
        L.append(int(math.floor(x * 10 ** (14) % n)))
    return L


def list_reduced(L):
    R = []
    for i in L:
        if not i in R:
            R.append(i)
    return R


def set_diff(L1, L2):
    for i in range(len(L2)):
        L1.remove(L2[i])
    return L1


def perm(L, ind):
    pos = []
    for i in range(len(ind)):
        pos.append(L[ind[i]])
    return pos


def random_list(x, p, L):
    pos = []
    ind = []
    ind = list_reduced(chaotic_map(x, p, len(L)))
    pos = perm(L, ind)
    if len(pos) == len(L):
        return pos
    elif len(pos) == 1:
        return L
    else:
        return pos + random_list(x, p, set_diff(L, pos))
    return pos


def permuted_pos(binary_seq, x, p):
    pos = []
    rlist = random_list(x, p, list(range(64)))
    for i in range(len(rlist)):
        if binary_seq[i] == "1":
            pos.append(rlist[i])
    if len(pos) != 64:
        pos.extend(random_list(x, p, set_diff(rlist, pos)))
    return pos


def replace(byte_init, bit):
    if bit == '0':
        if byte_init % 2 == 0:
            byte_fin = byte_init
        else:
            byte_fin = byte_init - 1
    elif bit == '1':
        if byte_init % 2 == 0:
            byte_fin = byte_init + 1
        else:
            byte_fin = byte_init
    return byte_fin


def vector2matrix(vect, n):
    m = len(vect) // n
    dims = (m, n)
    M = np.zeros(dims)
    for i in range(m):
        j = i * n
        k = (i + 1) * n
        M[i][:] = vect[j:k]
    return M


def mzig_zag_scan(vect):
    L = np.zeros(len(vect))
    pos = vzig_zag_scan(vector2matrix(list(range(64)), 8))
    for i in range(len(pos)):
        L[int(pos[i])] = vect[i]
    return vector2matrix(L, 8)


def divide_elem_matrix(A, Q):
    dims = (len(A), len(A[1]))
    M = np.zeros(dims)
    for i in range(len(A)):
        for j in range(len(A[1])):
            M[i][j] = A[i][j] / Q[i][j]
    return M


def quantpq(A, QF):
    if QF > 50:
        F = (100 - QF) / 50
    else:
        F = 50 / QF
    Q = np.array([
        [16, 11*F, 10*F, 16*F, 24, 40, 51, 61],
        [12*F, 12*F, 14*F, 19, 26, 58, 60, 55],
        [14*F, 13*F, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]])
    return divide_elem_matrix(A, Q)


def quantinvpq(A, QF):
    if QF > 50:
        F = (100 - QF) / 50
    else:
        F = 50 / QF
    Q = np.array([
        [16, 11*F, 10*F, 16*F, 24, 40, 51, 61],
        [12*F, 12*F, 14*F, 19, 26, 58, 60, 55],
        [14*F, 13*F, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]])
    return prod_elem_matrix(A, Q)


def prod_elem_matrix(A, Q):
    dims = (len(A), len(A[1]))
    M = np.zeros(dims)
    for i in range(len(A)):
        for j in range(len(A[1])):
            M[i][j] = A[i][j] * Q[i][j]
    return M


def ext_lsb(byte):
    if byte % 2 == 0:
        LSB = '0'
    else:
        LSB = '1'
    return LSB


class MyQR62:

    def __init__(self):
        self.myqr = np.ndarray(shape=(62, 62))
        for x in range(62):
            for y in range(62):
                self.myqr[x, y] = 100

    def get_data(self):    # Devuelve una lista con los datos

        return None

    def set_data(self, lista):    # Asigna los datos correspondientes a los valores de lista

        return None

    def get_resconstructed(self, qr_array):
        qr_estandar = self.get_qr()
        for i in range(62):
            for j in range(62):
                if qr_estandar[i, j] == 100:
                    qr_estandar[i, j] = qr_array[i, j]
        return qr_estandar

    def get_qr(self):  # Devuelve array correspondiente a la imagen del QR Code
        # Franja blanca de arriba y abajo
        for i in range(6):
            for y in range(62):
                self.myqr[i, y] = 255
                self.myqr[56+i, y] = 255

        # Franja blanca de la izquierda y derecha
        for i in range(62):
            for y in range(6):
                self.myqr[i, y] = 255
                self.myqr[i, 61-y] = 255

        # Cuadro superior izquierdo
        self.myqr[6:22, 6:22] = 255  # Blanco
        self.myqr[6:20, 6:20] = 0  # Negro
        self.myqr[8:18, 8:18] = 255  # Blanco
        self.myqr[10:16, 10:16] = 0  # Negro

        # Cuadro superior derecho
        self.myqr[6:22, 40:56] = 255  # Blanco
        self.myqr[6:20, 42:56] = 0  # Negro
        self.myqr[8:18, 44:54] = 255  # Blanco
        self.myqr[10:16, 46:52] = 0  # Negro

        # Cuadro inferiro izquierdo
        self.myqr[40:56, 6:22] = 255  # Blanco
        self.myqr[42:56, 6:20] = 0  # Negro
        self.myqr[44:54, 8:18] = 255  # Blanco
        self.myqr[46:52, 10:16] = 0  # Blanco

        # Cuadro pequeno inferior derecha
        self.myqr[38:48, 38:48] = 0  # Negro
        self.myqr[40:46, 40:46] = 255  # Blanco
        self.myqr[42:44, 42:44] = 0  # Negro

        # Puntos de alineamiento
        self.myqr[22:24, 18:20] = 0
        self.myqr[24:26, 18:20] = 255
        self.myqr[26:28, 18:20] = 0
        self.myqr[28:30, 18:20] = 255
        self.myqr[30:32, 18:20] = 0
        self.myqr[32:34, 18:20] = 255
        self.myqr[34:36, 18:20] = 0
        self.myqr[36:38, 18:20] = 255
        self.myqr[38:40, 18:20] = 0

        self.myqr[18:20, 22:24] = 0
        self.myqr[18:20, 24:26] = 255
        self.myqr[18:20, 26:28] = 0
        self.myqr[18:20, 28:30] = 255
        self.myqr[18:20, 30:32] = 0
        self.myqr[18:20, 32:34] = 255
        self.myqr[18:20, 34:36] = 0
        self.myqr[18:20, 36:38] = 255
        self.myqr[18:20, 38:40] = 0

        return self.myqr


def extract(watermarked_filename):
    # Key input
    key = "N;fpr-y7hrcMste4"
    # Load cover image (array)
    watermarked_array = misc.fromimage(Image.open(watermarked_filename))
    # Blue plane
    B = watermarked_array[:, :, 2]
    # Initial values
    la, QF = -1, 77.0
    vac = []
    vac_aux = []
    list_param = [0.27, 0.33456289967845987, 1.99989888346577778, 8]
    x0, p = list_param[1], list_param[2]
    secrete_bits = ""
    # Instances
    dt = Dtop(13, 13)
    blocks_instance = BlocksImage(B)
    # Creating zero matrix
    dims = (blocks_instance.max_num_blocks(), 64)
    matrix_vac = np.zeros(dims)
    # Sub-keys
    Lkey = div_key(key)
    # Key expansion from sha512
    key_expansion = sha512_bin(Lkey[0]) + sha512_bin(Lkey[1])
    # Collecting AC coefficients
    for i in range(blocks_instance.max_num_blocks()):
        DCT_Coef = dt.dtop2(blocks_instance.get_block(i))
        matrix_vac[i, :] = vzig_zag_scan(quantpq(DCT_Coef, QF))
        vac.extend(matrix_vac[i, :][1:9])

    key_expansion = increase_string(key_expansion, len(vac))

    # Dividing into bloks of length 9
    N = len(vac) // 64

    # Extracting secrete bits
    for i in range(N):
        j = i * 64
        k = (i + 1) * 64
        vacp = vac[j:k]
        pos = permuted_pos(key_expansion[j:k], x0, p)
        for r in range(len(vacp)):
            secrete_bits += ext_lsb(abs(round(vacp[pos[r]])))

    # Conformando QR
    wh = int(math.sqrt(len(secrete_bits)))
    extract_image = Image.new("1", (wh, wh), 255)
    array_extract_image = misc.fromimage(extract_image)

    for i in range(wh):
        for y in range(wh):
            if secrete_bits[wh*i+y] == '0':
                array_extract_image[i, y] = 0

    myqr = MyQR62()
    return misc.toimage(myqr.get_resconstructed(array_extract_image))


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
        extract_watermark = extract(input_filename)
        extract_watermark.save(output_filename, quality=100)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
