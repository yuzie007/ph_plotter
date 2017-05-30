#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from ph_plotter.colormap_creator import ColormapCreator

__author__ = "Yuji Ikeda"


class Colorbar(object):
    def __init__(self, colors_p, colors_n, num_p, num_n):
        self._colors_p = colors_p
        self._colors_n = colors_n
        self._num_p = num_p
        self._num_n = num_n
        self._cmap = None

    def create_colormap(self):
        colormap_creator = ColormapCreator(
            colors_p=self._colors_p,
            colors_n=self._colors_n,
        )
        self._create_bounds()
        cmap = colormap_creator.create_colormap(ticks=self._bounds)

        self._cmap = cmap

    def _create_bounds(self):
        bounds = np.array(
            range(-self._num_n + 1, 0) + range(self._num_p)
        )
        self._bounds = bounds

    def plot(self, figsize, figure_type, save):
        cmap = self._cmap
        bounds = self._bounds
        fig, axarr = plt.subplots(
            1, 1,
            figsize=figsize,
            tight_layout=True)
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        mpl.colorbar.ColorbarBase(axarr, cmap=cmap, norm=norm, extend="both")

        if save:
            figure_name = "colorbar." + figure_type
            plt.savefig(figure_name, transparent=True)
        else:
            plt.show()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--cp", dest="colors_p",
                        nargs="+",
                        default="r",
                        type=str,
                        help="Colors in the positive region.")
    parser.add_argument("--cn", dest="colors_n",
                        nargs="+",
                        default="w",
                        type=str,
                        help="Colors in the negative region.")
    parser.add_argument("--np", dest="num_p",
                        default=1,
                        type=int,
                        help="Number of colors in the positive region.")
    parser.add_argument("--nn", dest="num_n",
                        default=1,
                        type=int,
                        help="Number of colors in the negative region.")
    parser.add_argument("-a", "--alpha",
                        default=0.2,
                        type=float,
                        help="Alpha for the color of low-frequency weights.")
    parser.add_argument("-t", "--figure_type",
                        default="pdf",
                        type=str,
                        help="Filetype of figures.")
    parser.add_argument("--figsize",
                        nargs=2,
                        default=(1.0, 4.0),
                        type=float,
                        help="Filesize of figures.")
    parser.add_argument("-s", "--save",
                        action="store_true",
                        help="Save the colorbar figure")
    args = parser.parse_args()

    colorbar = Colorbar(args.colors_p, args.colors_n, args.num_p, args.num_n)
    colorbar.create_colormap()
    colorbar.plot(args.figsize, args.figure_type, args.save)


if __name__ == "__main__":
    main()
