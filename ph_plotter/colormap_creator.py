#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import numpy as np
from matplotlib.colors import LinearSegmentedColormap, ListedColormap


def get_colormap_0(alpha=0.2):
    a = alpha
    cdict = {
        'red':   ((0.0, 1-a, 1-a),
                  (1.0, 1.0, 1.0)),

        'green': ((0.0, 1-a, 1-a),
                  (1.0, 0.0, 0.0)),

        'blue':  ((0.0, 1-a, 1-a),
                  (1.0, 0.0, 0.0)),

        'alpha': ((0.0,   a,   a),
                  (1.0, 1.0, 1.0)),
    }
    cmap = LinearSegmentedColormap("CustomMap", cdict)
    # cmap.set_under((0.0, 0.0, 1.0))
    # cmap.set_over ((0.0, 0.5, 0.0))
    return cmap


def get_colormap_1(alpha=0.2):
    a = alpha
    cdict = {
        'red': (
            (0.00, 0.0, 1.0),
            (0.25, 0.0, 0.0),
            (0.50, 0.0, 0.0),
            (0.75, 1.0, 1.0),
            (1.00, 1.0, 1.0),
        ),
        'green': (
            (0.00, 0.0, 1.0),
            (0.25, 0.0, 0.0),
            (0.50, 1.0, 1.0),
            (0.75, 1.0, 1.0),
            (1.00, 0.0, 0.0),
        ),
        'blue': (
            (0.00, 1.0, 1.0),
            (0.25, 1.0, 1.0),
            (0.50, 0.0, 0.0),
            (0.75, 0.0, 0.0),
            (1.00, 0.0, 0.0),
        ),
        'alpha': (
            (0.00, 1.0, 1.0),
            (1.00, 1.0, 1.0),
        ),
    }
    cmap = LinearSegmentedColormap("CustomMap", cdict)
    cmap.set_under((1.0, 1.0, 1.0))
    cmap.set_over ((1.0, 0.0, 0.0))
    return cmap


def get_colormap_2(alpha=0.2):
    a = alpha
    cdict = {
        'red': (
            (0.0, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            (1.0, 1.0, 1.0),
        ),
        'green': (
            (0.0, 1.0, 0.0),
            (0.5, 1.0, 1.0),
            (1.0, 0.5, 0.0),
        ),
        'blue': (
            (0.0, 1.0, 0.5),
            (0.5, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        ),
        'alpha': (
            (0.0, 1.0, 1.0),
            (0.5, 1.0, 1.0),
            (1.0, 1.0, 1.0),
        ),
    }
    cmap = LinearSegmentedColormap("CustomMap", cdict)
    cmap.set_under((0.0, 0.0, 1.0))
    cmap.set_over ((0.0, 0.5, 0.0))
    return cmap


class ColormapCreator(object):
    def create_colormap(self, colorname="red", alpha=1.0, ncolor=10):
        from matplotlib.colors import ColorConverter

        color_tuple = ColorConverter().to_rgba(colorname)

        color_list = np.zeros((ncolor, 4))
        white = np.array((1.0, 1.0, 1.0, alpha))
        diff = (np.array(color_tuple) - white) / ncolor
        for i in range(ncolor):
            color_list[i] = white + diff * i

        # Transparent
        color_list[0] = [0.0, 0.0, 0.0, 0.0]

        print("color_list:")
        print(color_list)

        cmap = ListedColormap(color_list)
        cmap.set_under(color_list[0])
        cmap.set_over(color_tuple)
        return cmap
