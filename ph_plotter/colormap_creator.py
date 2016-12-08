#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import numpy as np
from matplotlib.colors import ColorConverter, ListedColormap


class ColormapCreator(object):
    def __init__(self, color_p='r', color_n='w', alpha=1.0, is_transparent_gradient=False):
        self._alpha = alpha
        self._color_p = color_p
        self._color_n = color_n
        self._is_transparent_gradient = is_transparent_gradient

    def create_colormap(self, values, prec=1e-6):
        color_p = self._color_p
        color_n = self._color_n
        ncolor_p = len(np.where(values >  prec)[0])
        ncolor_n = len(np.where(values < -prec)[0])

        color_list_0 = np.array([[0.0, 0.0, 0.0, 0.0]])
        color_list_n = self.create_color_list(color_n, ncolor_n)
        color_list_n = color_list_n[::-1]
        color_list_n = np.vstack((color_list_n, color_list_0))
        color_list_p = self.create_color_list(color_p, ncolor_p)
        color_list_p = np.vstack((color_list_0, color_list_p))

        color_list = np.vstack((color_list_n, color_list_p))
        color_list = self.convert_white_to_transparent(color_list)

        print("color_list:")
        print(color_list)

        cmap = ListedColormap(color_list[1:-1])
        cmap.set_under(color_list[0])
        cmap.set_over(color_list[-1])
        return cmap

    def create_color_list(self, colorname, ncolor):
        color_array = ColorConverter().to_rgba(colorname)
        color_array = np.array(color_array)

        color_list = np.zeros((ncolor, 4))
        if ncolor > 0:
            white_array = self.create_white_array(color_array)
            diff = (color_array - white_array) / ncolor
            for i in range(ncolor):
                color_list[i] = white_array + diff * (i + 1)

        return color_list

    def create_white_array(self, color_array):
        alpha = self._alpha
        if self._is_transparent_gradient:
            white_array = np.copy(color_array)
            white_array[3] = 0.0  # transparent
        else:
            white_array = np.array((1.0, 1.0, 1.0, alpha))
        return white_array

    def create_colormap_old(self, colorname="red", alpha=1.0, ncolor=10):
        color_array = ColorConverter().to_rgba(colorname)
        color_array = np.array(color_array)

        color_list = np.zeros((ncolor, 4))
        white_array = np.array((1.0, 1.0, 1.0, alpha))
        diff = (color_array - white_array) / ncolor
        for i in range(ncolor):
            color_list[i] = white_array + diff * i

        # Transparent
        color_list[0] = [0.0, 0.0, 0.0, 0.0]

        print("color_list:")
        print(color_list)

        cmap = ListedColormap(color_list)
        cmap.set_under(color_list[0])
        cmap.set_over(color_array)
        return cmap

    @staticmethod
    def convert_white_to_transparent(color_list):
        white = np.array([1.0, 1.0, 1.0])
        prec = 1e-3
        for i, color in enumerate(color_list):
            if np.all(np.abs(color[:3] - white) < prec):
                color_list[i] = [0.0, 0.0, 0.0, 0.0]
        return color_list
