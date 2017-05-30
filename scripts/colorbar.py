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
    def create_colormap(self, colors_p, colors_n, crange, cpitch):
        self._create_bounds(crange, cpitch)

        colormap_creator = ColormapCreator(colors_p=colors_p, colors_n=colors_n)
        cmap = colormap_creator.create_colormap(ticks=self._bounds)

        self._cmap = cmap

    def _create_bounds(self, crange, cpitch):
        n = int(round((crange[1] - crange[0]) / cpitch)) + 1
        bounds = np.linspace(crange[0], crange[1], n)
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
    parser.add_argument("--range",
                        nargs=2,
                        default=[-1.0, 1.0],
                        type=float,
                        help="Plotting range")
    parser.add_argument("--pitch",
                        default=1.0,
                        type=float,
                        help="Plotting pitch")
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

    colorbar = Colorbar()
    colorbar.create_colormap(args.colors_p, args.colors_n, args.range, args.pitch)
    colorbar.plot(args.figsize, args.figure_type, args.save)


if __name__ == "__main__":
    main()
