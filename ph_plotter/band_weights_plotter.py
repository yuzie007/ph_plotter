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


class BandWeightsPlotter(Plotter):
    def load_data(self, data_file="band.hdf5"):
        print("Reading band.hdf5: ", end="")
        distances, frequencies, pr_weights, nstars = read_band_hdf5(data_file)
        print("Finished")

        self._distances = distances
        self._frequencies = frequencies
        self._pr_weights = pr_weights
        self._nstars = nstars

        band_labels = read_band_labels("band.conf")
        print("band_labels:", band_labels)
        self._band_labels = band_labels

        return self

    def plot(self, ax):
        variables = self._variables

        distances = self._distances / self._distances[-1, -1]  # normalization
        frequencies = self._frequencies
        pr_weights = self._pr_weights

        freq_label = "Frequency ({})".format(variables["freq_unit"])
        d_freq = variables["d_freq"]
        f_min = variables["f_min"]
        f_max = variables["f_max"]
        n_freq = int((f_max - f_min) / d_freq) + 1

        ml = AutoMinorLocator(2)
        ax.yaxis.set_minor_locator(ml)

        ax.set_xticks([0.0] + list(distances[:, -1]))
        ax.set_xticklabels(self._band_labels)
        ax.set_xlabel("Wave vector")
        ax.set_xlim(distances[0, 0], distances[-1, -1])

        ax.set_yticks(np.linspace(f_min, f_max, n_freq))
        ax.set_ylabel(freq_label)
        ax.set_ylim(f_min, f_max)

        for x in [0.0] + list(distances[:, -1]):
            ax.axvline(x, color="k", dashes=(2, 2), linewidth=0.5)
        # for y in np.linspace(f_min, f_max, n_freq):
        #     ax.axhline(y, color="#000000", linestyle=":")
        ax.axhline(0, color="k", dashes=(2, 2), linewidth=0.5)  # zero axis

        n_sf = 10

        points = []
        npath, nqpoint, nstar, nband = frequencies.shape
        for ipath in range(npath):
            for i, d in enumerate(distances[ipath]):
                f = frequencies[ipath, i]
                w = pr_weights[ipath, i]
                tmp = np.stack(
                    (np.ones((nstar, nband)) * d, f, w)
                ).T.reshape((nstar * nband, -1))
                points.extend(tmp)
        points = np.array(points)

        self._colormap = ColormapCreator().create_colormap_old(
            colorname=variables["colormap"],
            alpha=variables["alpha"],
            ncolor=n_sf)
        PC = ax.scatter(
            points[:, 0],
            points[:, 1] * variables["unit"],
            c=points[:, 2],
            s=5.0,  # size
            edgecolors="None",
            cmap=self._colormap,
            vmin=0.0,
            vmax=1.0,
            rasterized=True,
        )
        self._quad_mesh = PC

    def create_figure_name(self):
        variables = self._variables
        figure_name = "band_weights_{}.{}".format(
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
            self._quad_mesh, extend="both")
        cb_label = "Weight"
        colorbar.set_label(
            cb_label,
            verticalalignment="baseline",
            rotation=-90)
