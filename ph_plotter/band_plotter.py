#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

__author__ = "Yuji Ikeda"

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from .plotter import Plotter, read_band_labels


def read_band_yaml(yaml_file="band.yaml"):
    import yaml
    data = yaml.load(open(yaml_file, "r"))
    nqpoint = data['nqpoint']
    npath = data['npath']
    natom = data['natom']
    nband = natom * 3
    nsep = nqpoint // npath
    distance = np.zeros((npath, nsep))
    frequency = np.zeros((npath, nsep, nband))
    for ipath in range(npath):
        for isep in range(nsep):
            iq = ipath * nsep + isep
            distance[ipath, isep] = data['phonon'][iq]['distance']
            for iband in range(nband):
                frequency[ipath, isep, iband] = (
                    data['phonon'][iq]['band'][iband]['frequency']
                )
    return distance, frequency


class BandPlotter(Plotter):
    def load_data(self, data_file="band.yaml"):
        print("Reading band.yaml: ", end="")
        distances, frequencies = read_band_yaml(yaml_file=data_file)
        print("Finished")

        self._distances = distances
        self._frequencies = frequencies

        band_labels = read_band_labels("band.conf")
        print("band_labels:", band_labels)
        self._band_labels = band_labels

        return self

    def plot(self):
        variables = self._variables

        distances = self._distances
        frequencies = self._frequencies

        freq_label = "Frequency ({})".format(variables["freq_unit"])
        d_freq = variables["d_freq"]
        f_min = variables["f_min"]
        f_max = variables["f_max"]
        n_freq = int((f_max - f_min) / d_freq) + 1

        fontsize = 12
        params = {
            "font.family": "Arial",
            "font.size": fontsize,
            "mathtext.fontset": "custom",
            "mathtext.it": "Arial",
        }
        plt.rcParams.update(params)

        plt.figure(
            figsize=variables["figsize"],
            frameon=False,
            tight_layout=True,
        )

        ml = AutoMinorLocator(2)
        plt.axes().yaxis.set_minor_locator(ml)

        plt.xticks([0.0] + list(distances[:, -1]), self._band_labels)
        plt.xlabel("Wave vector")
        plt.xlim(distances[0, 0], distances[-1, -1])

        plt.yticks(np.linspace(f_min, f_max, n_freq))
        plt.ylabel(freq_label)
        plt.ylim(f_min, f_max)

        for x in [0.0] + list(distances[:, -1]):
            plt.axvline(x, color="k", dashes=(2, 2), linewidth=0.5)
        # for y in np.linspace(f_min, f_max, n_freq):
        #     plt.axhline(y, color="#000000", linestyle=":")
        plt.axhline(0, color="k", dashes=(2, 2), linewidth=0.5)  # zero axis

        npath, nqpoint, nband = frequencies.shape
        for ipath in range(npath):
            lines = plt.plot(
                distances[ipath],
                frequencies[ipath] * variables["unit"],
                variables["linecolor"],
                dashes=variables["dashes"],
                linewidth=variables["linewidth"],
            )

        figure_name = "band_{}.{}".format(
            variables["freq_unit"],
            variables["figure_type"],
        )
        plt.savefig(figure_name, transparent=True)
        plt.close()
