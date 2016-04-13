#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

from ph_plotter.common_arguments_adder import CommonArgumentsAdder


def run(variables):
    from ph_plotter.band_weights_plotter import BandWeightsPlotter
    BandWeightsPlotter(variables).run()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    CommonArgumentsAdder().add_common_arguments(parser)
    parser.add_argument("--data_file",
                        default="band.hdf5",
                        type=str,
                        help="Filename of data.")
    args = parser.parse_args()

    print("This script may not be useful.")

    print(vars(args))
    run(vars(args))


if __name__ == "__main__":
    main()
