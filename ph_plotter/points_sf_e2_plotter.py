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

        elements = self._data_points[iq]['elements']

        partial_sf = self._data_points[iq]['partial_sf_e2']
        sf_elements = np.sum(partial_sf, axis=1)

        for i, label in enumerate(elements):
            sf = sf_elements[:, i]
            self._plot_curve(ax, iq, sf, label=label)

        return

    def create_figure_name(self):
        variables = self._variables
        figure_name = "points_sf_e2_{}.{}".format(
            variables["freq_unit"],
            variables["figure_type"])
        return figure_name
