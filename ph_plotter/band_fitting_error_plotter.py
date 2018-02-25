#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from .band_width_plotter import BandWidthPlotter

__author__ = 'Yuji Ikeda'


class BandFittingErrorPlotter(BandWidthPlotter):
    def plot(self, ax):
        variables = self._variables
        distances = self._distances
        fiterrs = self._fiterrs

        nq, nband = fiterrs.shape
        lines = ax.plot(
            distances.flatten(),
            fiterrs / variables["unit"],
            # variables["linecolor"],
            # dashes=variables["dashes"],
        )
        ax.set_ylabel('')
        return lines

    def create_figure_name(self):
        return "band_fitting_error.{}".format(self._variables["figure_type"])
