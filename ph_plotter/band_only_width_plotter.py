#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from .band_width_plotter import BandWidthPlotter

__author__ = 'Yuji Ikeda'


class BandOnlyWidthPlotter(BandWidthPlotter):
    def _set_is_sorted(self):
        self._is_sorted = False

    def plot(self, ax):
        variables = self._variables
        distances = self._distances
        frequencies = self._frequencies
        bandwidths = self._bandwidths

        npath, nqpoint, nband = frequencies.shape
        for ipath in range(npath):
            for ib in range(nband):
                ax.plot(
                    distances[ipath],
                    bandwidths[ipath, :, ib] * 2.0 * variables["unit"],
                    alpha=variables['alpha'],
                )

    def create_figure_name(self):
        return "band_only_width.{}".format(self._variables["figure_type"])
