#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np


class DqKT:
    """
    Transformada Discreta de Krawtchouk
    """

    def __init__(self):
        coef0 = np.array([0.0669182, 0.181935, 0.333578, 0.46961, 0.527532, 0.472859, 0.325442, 0.151051])
        coef1 = np.array([0.191235, 0.388597, 0.471368,  0.323351, -0.0202087, -0.363246, -0.48874, -0.338313])
        coef2 = np.array([0.357657, 0.473562, 0.222594, -0.215771, -0.407057, -0.123127, 0.353475, 0.495899])
        coef3 = np.array([0.49842, 0.296162, -0.236366, -0.369437, 0.0838858, 0.413053, 0.0225738, -0.541622])
        coef4 = np.array([0.537856, -0.0851108, -0.404159, 0.107868, 0.38164, -0.179119, -0.37539, 0.458079])
        coef5 = np.array([0.449447, -0.419763, -0.0585517, 0.412412, -0.200908, -0.285171, 0.486411, -0.300004])
        coef6 = np.array([0.279847, -0.485158, 0.412485, -0.0429201, -0.351539, 0.49078, -0.35839, 0.1464])
        coef7 = np.array([0.114035, -0.291713, 0.473503, -0.555255, 0.488852, -0.323131, 0.154305, -0.0467557])

        self.coef = np.array([coef0, coef1, coef2, coef3, coef4, coef5, coef6, coef7])

    def dqkt2(self, array):
        """
        2D DKT
        """
        dkt = np.ndarray(shape=(8, 8))
        for x in range(8):
            for y in range(8):
                dkt[x, y] = self.M(array, x, y)
        return dkt

    def idqkt2(self, array):
        """
        2D IDKT
        """
        idkt = np.ndarray(shape=(8, 8))
        for x in range(8):
            for y in range(8):
                idkt[x, y] = self.IM(array, x, y)
        return idkt

    def M(self, A, m, n):
        M = 0
        for x in range(8):
            for y in range(8):
                M += ((self.coef[x, m]*self.coef[y, n]))*float(A[x, y])
        return M

    def IM(self, A, m, n):
        IM = 0
        for x in range(8):
            for y in range(8):
                IM += float(A[x, y])*self.coef[m, x]*self.coef[n, y]
        return IM
