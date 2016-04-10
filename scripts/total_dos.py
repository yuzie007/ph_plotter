#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

__author__ = "Yuji Ikeda"


def run(variables):
    from ph_plotter.total_dos_plotter import TotalDOSPlotter
    TotalDOSPlotter(variables).run()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--f_max",
                        default=10.0,
                        type=float,
                        help="Maximum plotted frequency (THz).")
    parser.add_argument("--f_min",
                        default=-2.5,
                        type=float,
                        help="Minimum plotted frequency (THz).")
    parser.add_argument("--d_freq",
                        default=2.5,
                        type=float,
                        help="Pitch for frequency (THz).")
    parser.add_argument("--linecolor",
                        default="#ff0000",
                        type=str,
                        help="Linecolor.")
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
    parser.add_argument("--data_file",
                        default="total_dos.dat",
                        type=str,
                        help="Filename of data.")
    args = parser.parse_args()

    print(vars(args))
    run(vars(args))


if __name__ == "__main__":
    main()
