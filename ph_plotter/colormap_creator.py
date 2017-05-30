#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import numpy as np
from matplotlib.colors import (
    ColorConverter, LinearSegmentedColormap, ListedColormap)


__author__ = "Yuji Ikeda"


def create_colors_interpolated(color_list, n):
    """

    Parameters
    ----------
    color_list : tuple
        list of colornames
    n : int
        number of interpolated colors

    Returns
    -------
    colors_interpolated

    """
    cmap = LinearSegmentedColormap.from_list(None, color_list)
    colors_interpolated = cmap(np.linspace(0, 1, n))
    return colors_interpolated


def convert_white_to_transparent(color_list):
    white = np.array([1.0, 1.0, 1.0])
    prec = 1e-3
    for i, color in enumerate(color_list):
        if np.all(np.abs(color[:3] - white) < prec):
            color_list[i] = [0.0, 0.0, 0.0, 0.0]
    return color_list


class ColormapCreator(object):
    def __init__(self, colors_p='r', colors_n='w', alpha=1.0, is_transparent_gradient=False):
        if isinstance(colors_p, basestring):
            colors_p = [colors_p]
        if isinstance(colors_n, basestring):
            colors_n = [colors_n]

        if is_transparent_gradient:
            color_zero = list(ColorConverter().to_rgba(colors_p[-1]))
            color_zero[3] = 0.0
        else:
            color_zero = (1.0, 1.0, 1.0, alpha)
        color_zero = [color_zero]

        self._colors_p = color_zero + colors_p
        self._colors_n = colors_n + color_zero

    def create_colormap_old_2(self, values, prec=1e-6):
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

    def create_colormap(self, ticks, prec=1e-6):
        ncolor_p = len(np.where(ticks >  prec)[0]) + 1  # including zero
        ncolor_n = len(np.where(ticks < -prec)[0]) + 1  # including zero

        colors_interpolated_p = create_colors_interpolated(self._colors_p, ncolor_p)
        colors_interpolated_n = create_colors_interpolated(self._colors_n, ncolor_n)
        colors = np.vstack((
            colors_interpolated_n,
            colors_interpolated_p,
        ))
        colors = convert_white_to_transparent(colors)

        print("colors:")
        print(colors)

        cmap = ListedColormap(colors[1:-1])
        cmap.set_under(colors[ 0])
        cmap.set_over (colors[-1])
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
