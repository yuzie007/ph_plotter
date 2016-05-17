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

    def plot(self, ax):
        self._object_plotted = self._plot_sf(ax, self._total_sf)

    def plot_selected_sf_irs(self, ax, irs_selected):
        """

        Parameters
        ----------
        ax : Matplotlib Axes object
        irs_selected : Dictionary
            Keys are for point groups, and values are for IRs to be plotted.
        """
        selected_sf_irs = self._create_selected_sf_irs(irs_selected)
        self._object_plotted = self._plot_sf(ax, selected_sf_irs)

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
