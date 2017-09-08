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

        npath, nqpoint, nband = fiterrs.shape
        for ipath in range(npath):
            lines = ax.plot(
                distances[ipath],
                fiterrs[ipath] / variables["unit"],
                # variables["linecolor"],
                # dashes=variables["dashes"],
            )
        ax.set_ylabel('')
