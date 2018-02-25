#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import numpy as np
from .band_width_plotter import BandWidthPlotter

__author__ = 'Yuji Ikeda'


class BandOnlyWidthPlotter(BandWidthPlotter):
    def _set_is_sorted(self):
        # This is to keep the order of IRs
        self._is_sorted = False

    def plot(self, ax):
        """

        Parameters
        ----------
        ax : Matplotlib Axes object
        """
        irs_selected = self._variables['selected_irreps']
        if irs_selected is not None:
            return self.plot_selected_irs(ax, irs_selected)
        else:
            return self.plot_all(ax)

    def plot_all(self, ax):
        sf = self._create_total_sf()
        return self._plot_width( ax, sf)

    def plot_selected_irs(self, ax, irs_selected):
        sf = self._create_selected_sf_irs(irs_selected)
        return self._plot_width(ax, sf)

    def _create_total_sf(self):
        return self._bandwidths

    def _plot_width(self, ax, widths):
        variables = self._variables

        nq, nband = widths.shape
        for ib in range(nband):
            ax.plot(
                self._distances.flatten(),
                widths[:, ib] * 2.0 * variables["unit"],
                dashes=variables['dashes'],
                alpha=variables['alpha'],
            )

    def _create_selected_sf_irs(self, irs_selected):
        from functools import reduce
        bandwidths = self._bandwidths

        pg_symbols = np.array(
            [str(x['pointgroup_symbol'], encoding='ascii') for x in self._data_points])
        masks = []
        for pg_selected in irs_selected:
            m0 = pg_symbols == pg_selected
            # Note: From numpy 1.13.0, we can use isin instead of in1d
            m1 = np.in1d(
                self._ir_labels, irs_selected[pg_selected]
            ).reshape(self._ir_labels.shape)
            masks.append(m0[:, None] & m1)
        mask = reduce(np.logical_or, masks)
        widths = self._bandwidths.copy()
        widths[~mask] = np.nan
        return widths

    def create_figure_name(self):
        return "band_only_width.{}".format(self._variables["figure_type"])
