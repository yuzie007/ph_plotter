#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import numpy as np
from ph_plotter.points_sf_plotter import PointsSFPlotter


__author__ = "Yuji Ikeda"


class PointsSFIRsPlotter(PointsSFPlotter):
    def _create_sf_filename(self, data_file):
        sf_filename = data_file.replace("band.hdf5", "sf_irreps.dat")
        return sf_filename

    def plot_q(self, ax, iq):
        lines_total = self.plot_total_q(ax, iq)
        lines_symbols = self.plot_irs_q(ax, iq)
        return lines_total, lines_symbols

    def plot_irs_q(self, ax, iq):

        variables = self._variables
        lines_symbols = []
        indices = self._find_nonzero_irs(iq)
        for index in indices:
            # ir_label = self._ir_labels[iq, index]
            ir_label = self._data_points[iq]['ir_labels'][index]
            ir_label = self._modify_ir_label(ir_label)
            sf_symbol = self._data_points[iq]['partial_sf_s'][:, index]

            if self._is_horizontal:
                xs = self._frequencies[iq] * variables["unit"]
                ys = sf_symbol
            else:
                xs = sf_symbol
                ys = self._frequencies[iq] * variables["unit"]

            linewidth = variables["linewidth"]
            lines = ax.plot(
                xs,
                ys,
                linewidth=linewidth,
                label=ir_label,
            )
            lines_symbols.append(lines)

        self._reset_prop_cycle(ax)

        return lines_symbols

    def create_figure_name(self):
        variables = self._variables
        figure_name = "points_sf_irreps_{}.{}".format(
            variables["freq_unit"],
            variables["figure_type"])
        return figure_name

    def _find_nonzero_irs(self, iq, prec=1e-6):
        num_irs = self._data_points[iq]['num_irreps']
        partial_sf = self._data_points[iq]['partial_sf_s']
        sum_sfs = np.sum(partial_sf[:, :num_irs], axis=0)
        indices = np.where(sum_sfs > prec)[0]
        return indices

    def _modify_ir_label(self, ir_label):
        if len(ir_label) == 1:
            return ir_label
        else:
            return ir_label[0] + "$_{{{}}}$".format(ir_label[1:])
