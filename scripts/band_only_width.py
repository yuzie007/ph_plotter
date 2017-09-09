#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from ph_plotter.common_arguments_adder import CommonArgumentsAdder

__author__ = 'Yuji Ikeda'


def run(variables):
    from ph_plotter.band_only_width_plotter import BandOnlyWidthPlotter
    BandOnlyWidthPlotter(variables).run()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    CommonArgumentsAdder().add_common_arguments(parser)
    parser.add_argument("--data_file",
                        default="sf_fit.hdf5",
                        type=str,
                        help="Filename of data.")
    args = parser.parse_args()

    print(vars(args))
    run(vars(args))


if __name__ == "__main__":
    main()
