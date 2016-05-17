#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import numpy as np
from ph_plotter.spectral_functions_plotter import SpectralFunctionsPlotter


class SFIRsPlotter(SpectralFunctionsPlotter):
    def _create_sf_filename(self, data_file):
        sf_filename = data_file.replace(
            "band.hdf5", "spectral_functions_irs.dat")
        return sf_filename

    def plot_q(self, ax, iq):
        lines_total = self.plot_total_q(ax, iq)
        lines_symbols = self.plot_irs_q(ax, iq)
        return lines_total, lines_symbols

    def plot_irs_q(self, ax, iq):
        from .attributes import colors, tuple_dashes

        variables = self._variables
        lines_symbols = []
        indices = self._find_nonzero_irs(iq)
        for counter, index in enumerate(indices):
            ir_label = self._ir_labels[iq, index]
            ir_label = self._modify_ir_label(ir_label)
            sf_symbol = self._partial_density[index, iq]

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
                label=ir_label,
            )
            lines_symbols.append(lines)

        return lines_symbols

    def create_figure_name(self):
        variables = self._variables
        figure_name = "spectral_functions_irs_{}.{}".format(
            variables["freq_unit"],
            variables["figure_type"])
        return figure_name

    def _find_nonzero_irs(self, iq, prec=1e-6):
        num_irs = self._num_irs[iq]
        sum_sfs = np.sum(self._partial_density[:num_irs, iq], axis=1)
        indices = np.where(sum_sfs > prec)[0]
        return indices

    def _modify_ir_label(self, ir_label):
        if len(ir_label) == 1:
            return ir_label
        else:
            return ir_label[0] + "$_{{{}}}$".format(ir_label[1:])
