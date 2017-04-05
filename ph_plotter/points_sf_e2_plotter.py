#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import numpy as np
from ph_plotter.points_sf_plotter import PointsSFPlotter


__author__ = "Yuji Ikeda"


class PointsSFE2Plotter(PointsSFPlotter):
    def plot_q(self, ax, iq):
        if True:
            lines_total = self.plot_total_q(ax, iq)
            lines_symbols = self.plot_elements_q(ax, iq)
        return lines_total, lines_symbols

    def plot_elements_q(self, ax, iq):

        variables = self._variables
        elements = self._data_points[iq]['elements']

        partial_sf = self._data_points[iq]['partial_sf_e2']
        sf_elements = np.sum(partial_sf, axis=1)

        lines_symbols = []
        for i, label in enumerate(elements):
            sf = sf_elements[:, i]

            if self._is_horizontal:
                xs = self._frequencies[iq] * variables["unit"]
                ys = sf
            else:
                xs = sf
                ys = self._frequencies[iq] * variables["unit"]

            linewidth = variables["linewidth"]
            lines = ax.plot(
                xs,
                ys,
                linewidth=linewidth,
                label=label,
            )
            lines_symbols.append(lines)

        self._reset_prop_cycle(ax)

        return lines_symbols

    def create_figure_name(self):
        variables = self._variables
        figure_name = "points_sf_e2_{}.{}".format(
            variables["freq_unit"],
            variables["figure_type"])
        return figure_name
