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


def get_colormap(colorname="red", alpha=0.2):
    color_list = []
    values = [1.00, 0.90, 0.80, 0.70, 0.65, 0.60, 0.55, 0.50, 0.45, 0.40]
    if colorname == "red":
        for v in values:
            color_list.append([1.0, v, v])
            cmap = ListedColormap(color_list)
            cmap.set_under((1.0, 1.0, 1.0))
            cmap.set_over ((1.0, 0.0, 0.0))
    elif colorname == "blue":
        for v in values:
            color_list.append([v, v, 1.0])
            cmap = ListedColormap(color_list)
            cmap.set_under((1.0, 1.0, 1.0))
            cmap.set_over ((0.0, 0.0, 1.0))
    return cmap


class ColormapCreator(object):
    def create_colormap(self, colorname="red", alpha=0.2):
        return get_colormap(colorname, alpha)
