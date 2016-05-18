#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

from ph_plotter.band_sf_plotter import BandSFPlotter


class BandSFMeshPlotter(BandSFPlotter):
    def _plot_sf(self, ax, sf):
        variables = self._variables

        # "pcolormesh" is much faster than "pcolor".
        quad_mesh = ax.pcolormesh(
            self._xs,
            self._ys * variables["unit"],
            sf,
            cmap=self._colormap,
            vmin=variables["sf_min"],
            vmax=variables["sf_max"],
            rasterized=True,  # This is important to make the figure light.
        )
        return quad_mesh
