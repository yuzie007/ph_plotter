#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import numpy as np
from matplotlib.ticker import AutoMinorLocator
from .plotter import Plotter, read_band_labels
from .file_io import read_band_hdf5
from .colormap_creator import ColormapCreator


class BandDensityPlotter(Plotter):
    def load_data(self, data_file="band.hdf5"):
        print("Reading band.hdf5: ", end="")
        distances, frequencies, pr_weights, nstars = read_band_hdf5(data_file)
        print("Finished")

        self._distances = distances
        self._frequencies = frequencies
        self._pr_weights = pr_weights
        self._nstars = nstars

        density_datafile = data_file.replace("band.hdf5", "density.dat")
        self.load_spectral_functions(density_datafile)

        band_labels = read_band_labels("band.conf")
        print("band_labels:", band_labels)
        self._band_labels = band_labels

        return self

    def configure(self, ax):
        variables = self._variables

        distances = self._distances / self._distances[-1, -1]  # normalization
        frequencies = self._frequencies
        pr_weights = self._pr_weights

        freq_label = "Frequency ({})".format(variables["freq_unit"])
        d_freq = variables["d_freq"]
        f_min = variables["f_min"]
        f_max = variables["f_max"]
        n_freq = int(round((f_max - f_min) / d_freq)) + 1

        ax.set_xticks([0.0] + list(distances[:, -1]))
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
        variables = self._variables

        # "pcolormesh" is much faster than "pcolor".
        PC = ax.contourf(
            self._xs / self._distances[-1, -1],  # normalization
            self._ys * variables["unit"],
            self._zs,
            cmap=self._colormap,
            vmin=sf_min,
            vmax=sf_max,
            levels=self._sf_ticks,
            extend="both",
            # rasterized=True,  # This is important to make the figure light.
        )
        self._quad_mesh = PC

    def create_figure_name(self):
        variables = self._variables
        figure_name = "band_density_{}.{}".format(
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
            self._quad_mesh, ax=ax, extend="both", ticks=self._sf_ticks)
        cb_label = "Spectral function (/{})".format(variables["freq_unit"])
        colorbar.set_label(
            cb_label,
            verticalalignment="baseline",
            rotation=-90)
