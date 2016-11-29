#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import numpy as np
from matplotlib.colors import ColorConverter, ListedColormap


class ColormapCreator(object):
    def create_colormap(self, values, colorname_p="red", colorname_n='white', alpha=1.0):
        prec = 1e-6
        ncolor_p = len(np.where(values >  prec)[0])
        ncolor_n = len(np.where(values < -prec)[0])

        color_list_0 = np.array([[0.0, 0.0, 0.0, 0.0]])
        color_list_n = self.create_color_list(colorname_n, alpha, ncolor_n)
        color_list_n = color_list_n[::-1]
        color_list_n = np.vstack((color_list_n, color_list_0))
        color_list_p = self.create_color_list(colorname_p, alpha, ncolor_p)
        color_list_p = np.vstack((color_list_0, color_list_p))

        color_list = np.vstack((color_list_n, color_list_p))
        color_list = self.convert_white_to_transparent(color_list)

        print("color_list:")
        print(color_list)

        cmap = ListedColormap(color_list[1:-1])
        cmap.set_under(color_list[0])
        cmap.set_over(color_list[-1])
        return cmap

    @staticmethod
    def create_color_list(colorname, alpha, ncolor):
        color_array = ColorConverter().to_rgba(colorname)
        color_array = np.array(color_array)

        color_list = np.zeros((ncolor, 4))
        if ncolor > 0:
            white_array = np.array((1.0, 1.0, 1.0, alpha))
            diff = (color_array - white_array) / ncolor
            for i in range(ncolor):
                color_list[i] = white_array + diff * (i + 1)

        return color_list

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
