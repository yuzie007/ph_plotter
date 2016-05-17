#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

from ph_plotter.common_arguments_adder import CommonArgumentsAdder


def run(variables):
    plot_style = variables.pop("plot_style")
    is_separated = variables.pop("is_separated")

    if plot_style == "mesh":
        from ph_plotter.band_sf_mesh_plotter import (
            BandSFMeshPlotter as BandSFPlotter)

    elif plot_style == "contour":
        from ph_plotter.band_sf_contour_plotter import (
            BandSFContourPlotter as BandSFPlotter)

    BandSFPlotter(variables, is_separated=is_separated).run()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    CommonArgumentsAdder().add_common_arguments(parser)
    parser.add_argument("--data_file",
                        default="band.hdf5",
                        type=str,
                        help="Filename of data.")
    parser.add_argument("--sf_with",
                        type=str,
                        choices=["elements", "irs"],
                        required=True,
                        help="To be plotted with total spectral functions.")
    parser.add_argument("--plot_style",
                        type=str,
                        choices=["mesh", "contour"],
                        required=True,
                        help="Plot style for spectral fucntions.")
    parser.add_argument("--sep", dest="is_separated",
                        action="store_true",
                        help="Spectral fucntions data is separated.")
    args = parser.parse_args()

    print(vars(args))
    run(vars(args))


if __name__ == "__main__":
    main()
