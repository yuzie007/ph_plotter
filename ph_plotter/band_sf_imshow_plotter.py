#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

from ph_plotter.band_sf_plotter import BandSFPlotter


class BandSFImshowPlotter(BandSFPlotter):
    def _plot_sf(self, ax, sf):
        variables = self._variables

        # "pcolormesh" is much faster than "pcolor".
        axes_image = ax.imshow(
            # self._xs / self._distances[-1, -1],  # normalization
            # self._ys * variables["unit"],
            sf.T,
            cmap=self._colormap,
            aspect="auto",
            vmin=variables["sf_min"],
            vmax=variables["sf_max"],
            origin="lower",
            extent=[0.0, 1.0, variables["f_min"], variables["f_max"]],
            # rasterized=True,  # This is important to make the figure light.
        )
        return axes_image
