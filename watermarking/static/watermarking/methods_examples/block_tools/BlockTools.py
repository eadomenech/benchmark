#!/usr/bin/env python
# -*- coding: utf-8 -*-

from transforms.Scipy_DCT import DCT


class BlockTools:
    """Esta clase implementa las acciones necesarias para dividir una matriz en bloques y
    el trabajo con dichos bloques.
    Métodos:
    max_blocks() - devuelve la cantidad de bloques que posee la matriz
    get_coord(num_block) - devuelve las coordenadas correspondientes al bloque número num_block
    get_block(num_block) - devuelve la matriz correspondiente al bloque número num_block
    set_block(block, num_block) - sustituye el bloque número num_block por el bloque block
    """

    # Método inicial
    def __init__(self, matrix, block_rows=8, block_colums=8):
        self.matrix = matrix
        self.block_rows = block_rows
        self.block_colums = block_colums
        self.blocks_in_rows = len(matrix[0]) // self.block_colums
        self.blocks_in_colums = len(matrix) // self.block_rows

    # Obtener el matrix
    def get(self):
        return self.matrix

    # Cantidad máxima de bloques NxM que posee una matriz
    def max_blocks(self):
        return self.blocks_in_rows * self.blocks_in_colums

    #  Obtener coordenadas correspondiente dado el número de bloque
    def get_coord(self, num_block):
        num_block -= 1
        if num_block < self.max_blocks:
            lista = []
            x1 = (num_block // self.blocks_in_rows)*self.block_rows
            x2 = x1 + self.block_rows - 1
            y1 = (num_block % self.blocks_in_rows)*self.block_colums
            y2 = y1 + self.block_colums - 1
            lista.append(x1)
            lista.append(x2)
            lista.append(y1)
            lista.append(y2)
            return lista
        raise Exception('Input array shape is not divisible by submatrix shape!')

    # Obtener el bloque num_block de una matriz
    # Los bloques se organizan de arriba hacia abajo y de izquierda a derecha
    # La numeración de los bloques comienzan en uno (1)
    def get_block(self, num_block):
        try:
            lista = self.get_coord(num_block)
            return self.matrix[lista[0]:lista[1]+1, lista[2]:lista[3]+1]
        except Exception:
            return None

    # Poner todos los pixel del bloque de un mismo color
    def set_color(self, num_block):
        try:
            lista = self.get_coord(num_block)

            blanco = 0
            negro = 0

            for x in range(lista[0], lista[1]+1):
                for y in range(lista[2], lista[3]+1):
                    if self.matrix[x, y] == 0:
                        negro += 1
                    else:
                        blanco += 1

            if negro > blanco:
                self.matrix[lista[0]:lista[1]+1, lista[2]:lista[3]+1] = 0
            else:
                self.matrix[lista[0]:lista[1]+1, lista[2]:lista[3]+1] = 255
            return None
        except Exception:
            return None

    # Sustituir el bloque num_block por block en una matriz dada
    def set_block(self, block, num_block):
        lista = self.get_coord(num_block)
        self.matrix[lista[0]:lista[1]+1, lista[2]:lista[3]+1] = block

    def split_submatrix(x, submat_shape, order='C'):
        p, q = submat_shape      # Store submatrix shape
        m, n = x.shape

        if np.any(np.mod(x.shape, np.array(submat_shape)) != 0):
            raise Exception('Input array shape is not divisible by submatrix shape!')

        if order == 'C':
            x4D = x.reshape(-1, p, n/q, q).transpose(0, 2, 1, 3).reshape(-1, p, q)
            return np.array_split(x4D, x.size/(p*q), axis=0)

        elif order == 'F':
            x2D = x.reshape(-1, n/q, q).transpose(1, 0, 2).reshape(-1, q)
            return np.array_split(x2D, x.size/(p*q), axis=0)

        else:
            print "Invalid output order."
            return x
