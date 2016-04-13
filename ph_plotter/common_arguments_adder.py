#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"


class CommonArgumentsAdder(object):
    def add_common_arguments(self, parser):
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
        parser.add_argument("--sf_max",
                            type=float,
                            help="Maximum of spectral functions.")
        parser.add_argument("--sf_min",
                            type=float,
                            help="Minimum of spectral functions.")
        parser.add_argument("--d_sf",
                            type=float,
                            help="Ticks of spectral functions.")
        parser.add_argument("--linecolor",
                            default="r",  # red
                            type=str,
                            help="Linecolor.")
        parser.add_argument("--colormap",  # red
                            default="r",
                            type=str,
                            help="Colors of the colormap.")
        parser.add_argument("-a", "--alpha",
                            default=1.0,
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
        parser.add_argument("--poscar",
                            default="POSCAR",
                            type=str,
                            help="Filename of POSCAR.")
