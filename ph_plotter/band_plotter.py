#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import numpy as np
from matplotlib.ticker import AutoMinorLocator
from .plotter import Plotter, read_band_labels
from .file_io import read_band_yaml


class BandPlotter(Plotter):
    def load_data(self, data_file="band.yaml"):
        print("Reading band.yaml: ", end="")
        distances, frequencies = read_band_yaml(yaml_file=data_file)
        print("Finished")

        self._distances = distances / distances[-1, -1]
        self._frequencies = frequencies
        print(np.min(frequencies), np.max(frequencies))

        band_labels = read_band_labels("band.conf")
        print("band_labels:", band_labels)
        self._band_labels = band_labels

        return self

    def configure(self, ax):
        variables = self._variables

        distances = self._distances

        freq_label = "Frequency ({})".format(variables["freq_unit"])
        d_freq = variables["d_freq"]
        f_min = variables["f_min"]
        f_max = variables["f_max"]
        n_freq = int(round((f_max - f_min) / d_freq)) + 1

        ax.set_xticks([0.0] + list(distances[:, -1]))
        if self._band_labels is not None:
            ax.set_xticklabels(self._band_labels)
        ax.set_xlabel("Wavevector")
        ax.set_xlim(distances[0, 0], distances[-1, -1])

        ax.set_yticks(np.linspace(f_min, f_max, n_freq))
        ax.set_ylabel(freq_label)
        ax.set_ylim(f_min, f_max)

        mly = AutoMinorLocator(2)
        ax.yaxis.set_minor_locator(mly)

        ax.grid(True, axis='x')
        # for y in np.linspace(f_min, f_max, n_freq):
        #     ax.axhline(y, color="#000000", linestyle=":")
        # zero axis
        ax.axhline(0, color="#b0b0b0", linewidth=0.8, zorder=0)

    def plot(self, ax):
        variables = self._variables
        distances = self._distances
        frequencies = self._frequencies

        npath, nqpoint, nband = frequencies.shape
        for ipath in range(npath):
            lines = ax.plot(
                distances[ipath],
                frequencies[ipath] * variables["unit"],
                color=variables["linecolor"],
                dashes=variables["dashes"],
                linewidth=variables["linewidth"],
            )

    def plot_selected_curve(self, ax, ipath, inum):
        variables = self._variables
        distances = self._distances
        frequencies = self._frequencies

        npath, nqpoint, nband = frequencies.shape
        lines = ax.plot(
            distances[ipath],
            frequencies[ipath, :, inum] * variables["unit"],
            variables["linecolor"],
            dashes=variables["dashes"],
            linewidth=variables["linewidth"],
        )

    def create_figure_name(self):
        variables = self._variables
        figure_name = "band_{}.{}".format(
            variables["freq_unit"],
            variables["figure_type"])
        return figure_name
