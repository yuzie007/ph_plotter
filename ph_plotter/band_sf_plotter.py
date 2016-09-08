#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import numpy as np
from matplotlib.ticker import AutoMinorLocator
from ph_plotter.plotter import read_band_labels
from ph_plotter.sf_plotter import SFPlotter
from ph_plotter.colormap_creator import ColormapCreator


class BandSFPlotter(SFPlotter):
    def _create_sf_filename(self, data_file):
        sf_type = self._variables["sf_with"]
        if sf_type == "elements":
            suffix = "elements"
        elif sf_type == "irreps":
            suffix = "irreps"
        else:
            raise ValueError("Invalid option for spectral function", sf_type)

        sf_filename = "sf_{}.dat".format(suffix)
        sf_filename = data_file.replace("band.hdf5", sf_filename)
        return sf_filename

    def configure(self, ax):
        variables = self._variables

        distances = self._distances / self._distances[-1, -1]  # normalization

        freq_label = "Frequency ({})".format(variables["freq_unit"])
        d_freq = variables["d_freq"]
        f_min = variables["f_min"]
        f_max = variables["f_max"]
        n_freq = int(round((f_max - f_min) / d_freq)) + 1

        ax.set_xticks([0.0] + list(distances[:, -1]))
        if self._band_labels is not None:
            ax.set_xticklabels(self._band_labels)
        ax.set_xlabel("Wave vector")
        ax.set_xlim(distances[0, 0], distances[-1, -1])

        ax.set_yticks(np.linspace(f_min, f_max, n_freq))
        ax.set_ylabel(freq_label)
        ax.set_ylim(f_min, f_max)

        sf_min = variables["sf_min"]
        sf_max = variables["sf_max"]
        d_sf = variables["d_sf"]
        nticks_sf = int(round((sf_max - sf_min) / d_sf))
        self._sf_ticks = np.linspace(sf_min, sf_max, nticks_sf + 1)

        mly = AutoMinorLocator(2)
        ax.yaxis.set_minor_locator(mly)

        for x in [0.0] + list(distances[:, -1]):
            ax.axvline(x, color="k", dashes=(2, 2), linewidth=0.5)
        # for y in np.linspace(f_min, f_max, n_freq):
        #     ax.axhline(y, color="#000000", linestyle=":")
        # zero axis
        ax.axhline(0, color="k", dashes=(2, 2), linewidth=0.5)

        self._colormap = ColormapCreator().create_colormap_new(
            values=self._sf_ticks,
            colorname_p=variables["colormap_p"],
            colorname_n=variables["colormap_n"],
            alpha=variables["alpha"],
        )

    def modify_data(self, distances, frequencies, sf):
        ninterp = self._variables["ninterp"]
        if ninterp is not None:
            distances, frequencies, sf = interpolate_data(
                distances, frequencies, sf, n=ninterp)
        return distances, frequencies, sf

    def plot(self, ax):
        """

        Parameters
        ----------
        ax : Matplotlib Axes object
        """
        irs_selected = self._variables['selected_irreps']
        combinations_elements = self._variables['combinations_elements']

        if irs_selected is not None and combinations_elements is not None:
            sf = self._create_selected_sf_irs_and_elements(irs_selected, combinations_elements)
        elif irs_selected is not None:
            sf = self._create_selected_sf_irs(irs_selected)
        elif combinations_elements is not None:
            sf = self._create_selected_sf_elements(combinations_elements)
        else:
            sf = self.create_total_sf()

        self._plot_sf_pre(ax, sf)

    def _plot_sf_pre(self, ax, sf):
        distances = self._xs
        frequencies = self._ys

        distances, frequencies, sf = self.modify_data(
            distances, frequencies, sf)

        self._object_plotted = self._plot_sf(
            ax, distances, frequencies, sf)

    def plot_selected_sf_irs(self, ax, irs_selected):
        """

        Parameters
        ----------
        ax : Matplotlib Axes object
        irs_selected : Dictionary
            Keys are for point groups, and values are for IRs to be plotted.
        """
        sf = self._create_selected_sf_irs(irs_selected)
        self._plot_sf_pre(ax, sf)

    def plot_sf_combinations_elements(self, ax, combinations_elements):
        sf = self._create_selected_sf_elements(combinations_elements)
        self._plot_sf_pre(ax, sf)

    def plot_sf_irs_and_elements(self, ax, selected_irs, combinations_elements):
        sf = self._create_selected_sf_irs_and_elements(selected_irs, combinations_elements)
        self._plot_sf_pre(ax, sf)

    def _create_selected_sf_irs(self, irs_selected):
        total_sf = self.create_total_sf()
        partial_sf = np.zeros_like(total_sf)  # Initialization
        for i, data_point in enumerate(self._data_points):
            ir_labels = data_point['ir_labels']
            pg_symbol = str(data_point['pointgroup_symbol'])
            if pg_symbol in irs_selected:
                for ir_label_selected in irs_selected[pg_symbol]:
                    indices = np.where(ir_labels == ir_label_selected)
                    for index in indices:
                        partial_sf[i] += data_point['partial_sf_s'][:, index[0]]
        return partial_sf

    def _create_selected_sf_irs_and_elements(self, irs_selected, combinations_elements):
        total_sf = self.create_total_sf()
        partial_sf = np.zeros_like(total_sf)  # Initialization
        for i, data_point in enumerate(self._data_points):
            elements = data_point['elements']
            ir_labels = data_point['ir_labels']
            pg_symbol = str(data_point['pointgroup_symbol'])
            if pg_symbol in irs_selected:
                for ir_label_selected in irs_selected[pg_symbol]:
                    indices = np.where(ir_labels == ir_label_selected)
                    for index in indices:
                        partial_sf_e = data_point['partial_sf_s_e'][:, index[0]]
                        partial_sf[i] += self._create_selected_sf_elements_point(
                            partial_sf_e, elements, combinations_elements)
        return partial_sf

    def _create_selected_sf_elements(self, combinations_elements):
        """Create partial sf for combinations of chemical elements

        Parameters
        ----------
        combinations_elements:  list of lists
            [['Cu', 'Cu'], ['Au', 'Au']]
        """
        total_sf = self.create_total_sf()
        partial_sf = np.zeros(total_sf.shape, dtype=complex)  # Initialization
        for i, data_point in enumerate(self._data_points):
            elements = data_point['elements']
            partial_sf_e = data_point['partial_sf_e']
            partial_sf[i] = self._create_selected_sf_elements_point(
                partial_sf_e, elements, combinations_elements)
        partial_sf = partial_sf.real
        return partial_sf

    @staticmethod
    def _create_selected_sf_elements_point(partial_sf_e, elements, combinations_elements):
        partial_sf_point = np.zeros(partial_sf_e.shape[0], dtype=complex)
        for combination_elements in combinations_elements:
            ie0 = list(elements).index(combination_elements[0])
            ie1 = list(elements).index(combination_elements[1])
            partial_sf_point += np.sum(partial_sf_e[:, :, ie0, :, ie1], axis=(1, 2))
            if ie0 != ie1:
                partial_sf_point += np.sum(partial_sf_e[:, :, ie1, :, ie0], axis=(1, 2))
        partial_sf_point = partial_sf_point.real
        return partial_sf_point

    def _plot_sf(self, ax, sf):
        raise NotImplementedError

    def create_figure_name(self):
        variables = self._variables
        figure_name = "band_sf_{}.{}".format(
            variables["freq_unit"],
            variables["figure_type"])
        return figure_name

    def save_figure(self, fig, figure_name):
        self.save_figure_without_colorbar(fig, figure_name)
        self.save_figure_with_colorbar(fig, figure_name)

    def save_figure_without_colorbar(self, fig, figure_name):
        fig.savefig(figure_name, dpi=288, transparent=True)

    def save_figure_with_colorbar(self, fig, figure_name):
        variables = self._variables

        colorbar = self.create_colorbar(fig)
        self.create_colorbar_label(colorbar)

        figure_name_w_bar = figure_name.replace(
            "." + variables["figure_type"],
            "_w_bar." + variables["figure_type"])
        fig.savefig(figure_name_w_bar, dpi=288, transparent=True)

    def create_colorbar(self, fig, cax=None, ax=None, **kwargs):
        colorbar = fig.colorbar(
            self._object_plotted,
            cax=cax,
            ax=ax,
            extend="both",
            ticks=self._sf_ticks,
            **kwargs)
        return colorbar

    def create_colorbar_label(self, colorbar, **kwargs):
        sf_label = self._create_sf_label()
        colorbar.set_label(
            sf_label,
            verticalalignment="baseline",
            rotation=-90,
            **kwargs)


def interpolate_data(xs, ys, zs, n):
    from scipy.interpolate import griddata

    xs_1d = xs[:, 0]
    ys_1d = ys[0, :]
    xs_fine_1d = create_fine_points(xs_1d, n)
    ys_fine_1d = create_fine_points(ys_1d, n)

    xs_fine, ys_fine = np.meshgrid(xs_fine_1d, ys_fine_1d)
    xs_fine = xs_fine.flatten()
    ys_fine = ys_fine.flatten()

    zs_fine = griddata(
        (xs.flatten(), ys.flatten()), zs.flatten(), (xs_fine, ys_fine),
        method="cubic")

    xs_fine = xs_fine.reshape(ys_fine_1d.size, xs_fine_1d.size).T
    ys_fine = ys_fine.reshape(ys_fine_1d.size, xs_fine_1d.size).T
    zs_fine = zs_fine.reshape(ys_fine_1d.size, xs_fine_1d.size).T

    return xs_fine, ys_fine, zs_fine


def create_fine_points(points, n):
    tmp = np.repeat(points, n)
    for i in range(n):
        tmp[i:-n:n] += np.diff(points) * i / float(n)
    points_fine = tmp[:1-n]
    return points_fine
