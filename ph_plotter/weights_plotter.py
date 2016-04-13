#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import numpy as np
from matplotlib.ticker import AutoMinorLocator
from matplotlib.backends.backend_pdf import PdfPages
from .plotter import Plotter
from .file_io import read_band_hdf5


class WeightsPlotter(Plotter):
    def load_data(self, data_file="band.hdf5"):
        print("Reading band.hdf5: ", end="")
        distances, frequencies, pr_weights, nstars = read_band_hdf5(data_file)
        print("Finished")

        self._distances = distances
        self._frequencies = frequencies
        self._pr_weights = pr_weights
        self._nstars = nstars

        return self

    def plot(self, ax):
        variables = self._variables

        distances = self._distances
        frequencies = self._frequencies
        pr_weights = self._pr_weights

        freq_label = "Frequency ({})".format(variables["freq_unit"])
        d_freq = variables["d_freq"]
        f_min = variables["f_min"]
        f_max = variables["f_max"]
        n_freq = int(round((f_max - f_min) / d_freq)) + 1

        mlx = AutoMinorLocator(2)
        ax.xaxis.set_minor_locator(mlx)

        ax.set_xticks(np.linspace(f_min, f_max, n_freq))
        ax.set_xlabel(freq_label)
        ax.set_xlim(f_min, f_max)

        mly = AutoMinorLocator(2)
        ax.yaxis.set_minor_locator(mly)

        ax.set_yticks(np.linspace(-0.2, 1.2, 8))
        ax.set_ylabel("Weight")
        ax.set_ylim(-0.2, 1.2)

        ax.axvline(0, color="k", dashes=(2, 2), linewidth=0.5)

        ax.axhline(0, color="k", dashes=(2, 2), linewidth=0.5)  # zero axis
        ax.axhline(1, color="k", dashes=(2, 2), linewidth=0.5)

        figure_name = self.create_figure_name()
        npath, nqpoint, nstar, nband = frequencies.shape
        pdf = PdfPages(figure_name)
        for ipath in range(npath):
            for i, d in enumerate(distances[ipath]):
                print(ipath, i)
                f = frequencies[ipath, i]
                w = pr_weights[ipath, i]

                PC = ax.scatter(
                    f * variables["unit"],
                    w,
                    c=variables["linecolor"],
                    s=10.0,  # size
                    edgecolors="None",
                )
                pdf.savefig(dpi=288, transparent=True)
                PC.remove()
        pdf.close()

    def create_figure_name(self):
        variables = self._variables
        figure_name = "weights_{}.{}".format(
            variables["freq_unit"],
            variables["figure_type"])
        return figure_name

    def save_figure(self, fig, figure_name):
        pass
