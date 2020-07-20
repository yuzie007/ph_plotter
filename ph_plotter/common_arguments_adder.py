#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"


class CommonArgumentsAdder(object):
    def add_common_arguments(self, parser):
        parser.add_argument("--f_max",
                            type=float,
                            help="Maximum plotted frequency (THz).")
        parser.add_argument("--f_min",
                            type=float,
                            help="Minimum plotted frequency (THz).")
        parser.add_argument("--d_freq",
                            type=float,
                            help="Pitch for frequency (THz).")
        parser.add_argument("--dos_max",
                            default=0.4,
                            type=float,
                            help="Maximum DOS (THz^-1).")
        parser.add_argument("--sf_max",
                            default=2.0,
                            type=float,
                            help="Maximum of spectral functions.")
        parser.add_argument("--sf_min",
                            default=0.0,
                            type=float,
                            help="Minimum of spectral functions.")
        parser.add_argument("--d_sf",
                            default=0.5,
                            type=float,
                            help="Ticks of spectral functions.")
        parser.add_argument("--linecolor",
                            type=str,
                            help="Linecolor.")
        parser.add_argument("--colormap_p",
                            default="r",
                            type=str,
                            help="Colors of the positive colormap.")
        parser.add_argument("--colormap_n",
                            default="b",
                            type=str,
                            help="Colors of the negative colormap.")
        parser.add_argument("--linewidth",
                            default=1.0,
                            type=float,
                            help="Linewidth.")
        parser.add_argument("--dashes",
                            nargs="+",
                            default=[],
                            type=float,
                            help="Dashes.")
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
                            help="Figure size.")
        parser.add_argument("--fontsize",
                            type=float,
                            help="Fontsize of figures.")
        parser.add_argument("--poscar",
                            default="POSCAR",
                            type=str,
                            help="Filename of POSCAR.")
