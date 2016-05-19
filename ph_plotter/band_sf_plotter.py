#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import numpy as np
from matplotlib.ticker import AutoMinorLocator
from ph_plotter.plotter import Plotter, read_band_labels
from ph_plotter.file_io import read_band_hdf5_dict
from ph_plotter.colormap_creator import ColormapCreator


class BandSFPlotter(Plotter):
    def load_data(self, data_file="band.hdf5"):
        print("Reading band.hdf5: ", end="")
        data = read_band_hdf5_dict(data_file)
        print("Finished")

        self._distances   = data["distances"]

        npath, nqp = self._distances.shape
        nq = npath * nqp

        if "frequencies" in data:
            self._frequencies = data["frequencies"]
        if "pr_weights" in data:
            self._pr_weights = data["pr_weights"]
        if "nqstars" in data:
            self._narms = data["nqstars"]
        if "rot_pr_weights" in data:
            self._rot_pr_weights = data["rot_pr_weights"]
        if "pg_symbols" in data:
            self._pg_symbols = data["pg_symbols"].reshape(nq)
        if "num_irs" in data:
            self._num_irs = data["num_irs"].reshape(nq)
        if "ir_labels" in data:
            self._ir_labels = data["ir_labels"].reshape(nq, -1)

        sf_filename = self._create_sf_filename(data_file)
        self.load_spectral_functions(sf_filename, npath, nqp)

        band_labels = read_band_labels("band.conf")
        print("band_labels:", band_labels)
        self._band_labels = band_labels

    def _create_sf_filename(self, data_file):
        if self._variables["sf_with"] == "elements":
            suffix = "atoms"
        elif self._variables["sf_with"] == "irs":
            suffix = "irs"
        else:
            raise ValueError("Invarid option for spectral function.")

        sf_filename = "spectral_functions_{}.dat".format(suffix)
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
        nticks_sf = int(round(sf_max / d_sf))
        self._sf_ticks = np.linspace(sf_min, sf_max, nticks_sf + 1)

        mly = AutoMinorLocator(2)
        ax.yaxis.set_minor_locator(mly)

        for x in [0.0] + list(distances[:, -1]):
            ax.axvline(x, color="k", dashes=(2, 2), linewidth=0.5)
        # for y in np.linspace(f_min, f_max, n_freq):
        #     ax.axhline(y, color="#000000", linestyle=":")
        # zero axis
        ax.axhline(0, color="k", dashes=(2, 2), linewidth=0.5)

        self._colormap = ColormapCreator().create_colormap(
            colorname=variables["colormap"],
            alpha=variables["alpha"],
            ncolor=nticks_sf)

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
        distances = self._xs
        frequencies = self._ys
        sf = self._total_sf

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
        distances = self._xs
        frequencies = self._ys
        sf = self._create_selected_sf_irs(irs_selected)

        distances, frequencies, sf = self.modify_data(
            distances, frequencies, sf)

        self._object_plotted = self._plot_sf(
            ax, distances, frequencies, sf)

    def _create_selected_sf_irs(self, irs_selected):
        selected_sf_irs = np.zeros_like(self._total_sf)  # Initialization
        for i, pg_symbol in enumerate(self._pg_symbols):
            if pg_symbol in irs_selected:
                for ir_label in irs_selected[pg_symbol]:
                    indices = np.where(self._ir_labels[i] == ir_label)
                    selected_sf_irs[i] += np.sum(
                        self._partial_density[:, i][indices], axis=0)
        return selected_sf_irs

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

        self.create_colorbar(fig)

        figure_name_w_bar = figure_name.replace(
            "." + variables["figure_type"],
            "_w_bar." + variables["figure_type"])
        fig.savefig(figure_name_w_bar, dpi=288, transparent=True)

    def create_colorbar(self, fig, ax=None):
        variables = self._variables

        colorbar = fig.colorbar(
            self._object_plotted, ax=ax, extend="both", ticks=self._sf_ticks)
        cb_label = "Spectral function (/{})".format(variables["freq_unit"])
        colorbar.set_label(
            cb_label,
            verticalalignment="baseline",
            rotation=-90)


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