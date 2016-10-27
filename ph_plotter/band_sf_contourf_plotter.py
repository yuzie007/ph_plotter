#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

from ph_plotter.band_sf_plotter import BandSFPlotter


class BandSFContourFPlotter(BandSFPlotter):
    def _plot_sf(self, ax, distances, frequencies, sf):
        variables = self._variables

        # "pcolormesh" is much faster than "pcolor".
        quad_contour_set = ax.contourf(
            distances,
            frequencies * variables["unit"],
            sf,
            cmap=self._colormap,
            linecolor="k",
            vmin=variables["sf_min"],
            vmax=variables["sf_max"],
            levels=self._sf_ticks,
            extend="both",
            # rasterized=True,  # This is important to make the figure light.
        )
        return quad_contour_set
