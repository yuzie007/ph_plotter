#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import numpy as np
from ph_plotter.points_sf_plotter import PointsSFPlotter


__author__ = "Yuji Ikeda"


class PointsSFAtomsPlotter(PointsSFPlotter):
    def plot_q(self, ax, iq):
        lines_total = self.plot_total_q(ax, iq)
        lines_symbols = self.plot_elements_q(ax, iq)
        return lines_total, lines_symbols

    def plot_elements_q(self, ax, iq):

        for counter, element_indices in enumerate(self._list_element_indices):
            element_label, indices = element_indices
            sf_symbol = np.sum(self._partial_sf[indices, iq], axis=0)

            self._plot_curve(ax, iq, sf_symbol, label=element_label)

        return

    def create_figure_name(self):
        variables = self._variables
        figure_name = "points_sf_atoms_{}.{}".format(
            variables["freq_unit"],
            variables["figure_type"])
        return figure_name
