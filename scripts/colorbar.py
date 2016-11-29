#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"


def run(variables):
    from ph_plotter.colormap_creator import ColormapCreator
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    cmap = ColormapCreator().create_colormap_old(
        colorname=variables["colormap"],
        ncolor=variables["ncolor"])
    fig, axarr = plt.subplots(
        1, 1,
        figsize=variables["figsize"],
        tight_layout=True)
    bounds = range(cmap.N + 1)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    mpl.colorbar.ColorbarBase(axarr, cmap=cmap, norm=norm, extend="both")

    figure_name = "colorbar." + variables["figure_type"]
    plt.savefig(figure_name, transparent=True)
    # plt.show()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--colormap",
                        default="r",
                        type=str,
                        help="Colors of the colormap.")
    parser.add_argument("--ncolor",
                        default=10,
                        type=int,
                        help="Number of colors in the colormap.")
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
                        default=(5.0, 3.5),
                        type=float,
                        help="Filesize of figures.")
    args = parser.parse_args()

    print(vars(args))
    run(vars(args))


if __name__ == "__main__":
    main()
