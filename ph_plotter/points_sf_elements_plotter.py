#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import numpy as np
from ph_plotter.points_sf_plotter import PointsSFPlotter


class PointsSFElementsPlotter(PointsSFPlotter):
    def _create_sf_filename(self, data_file):
        sf_filename = data_file.replace("band.hdf5", "sf_elements.dat")
        return sf_filename

    def plot_q(self, ax, iq):
        lines_total = self.plot_total_q(ax, iq)
        lines_symbols = self.plot_elements_q(ax, iq)
        return lines_total, lines_symbols

    def plot_elements_q(self, ax, iq):
        from .attributes import colors, tuple_dashes

        variables = self._variables
        natoms_primitive = self._data_points[iq]['natoms_primitive']
        elements         = self._data_points[iq]['elements'        ]

        lines_symbols = []
        for counter, element_label in enumerate(elements):
            slice_element = slice(counter, None, len(elements))
            sf_symbol = np.sum(self._partial_sf[slice_element, iq], axis=0)

            if self._is_horizontal:
                xs = self._ys[iq] * variables["unit"]
                ys = sf_symbol
            else:
                xs = sf_symbol
                ys = self._ys[iq] * variables["unit"]

            lines = ax.plot(
                xs,
                ys,
                color=colors[counter % len(colors)],
                dashes=tuple_dashes[counter % len(tuple_dashes)],
                linewidth=variables["linewidth"],
                label=element_label,
            )
            lines_symbols.append(lines)

        return lines_symbols

    def create_figure_name(self):
        variables = self._variables
        figure_name = "points_sf_elements_{}.{}".format(
            variables["freq_unit"],
            variables["figure_type"])
        return figure_name