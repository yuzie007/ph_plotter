#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import numpy as np
from matplotlib.ticker import AutoMinorLocator
from matplotlib.backends.backend_pdf import PdfPages
from .plotter import Plotter, read_band_labels
from .file_io import read_band_hdf5


class SpectralFunctionsPlotter(Plotter):
    def load_data(self, data_file="band.hdf5"):
        print("Reading band.hdf5: ", end="")
        distances, frequencies, pr_weights, nstars = read_band_hdf5(data_file)
        print("Finished")

        self._distances = distances
        self._frequencies = frequencies
        self._pr_weights = pr_weights
        self._nstars = nstars

        density_datafile = data_file.replace("band.hdf5", "density.dat")
        self.load_density(density_datafile)

        return self

    def load_density(self, filename="density.dat"):
        tmp = np.loadtxt(filename).T
        xs = tmp[0]
        ys = tmp[1]
        zs = tmp[2]
        n1, n2 = self._distances.shape
        n = n1 * n2
        self._xs = xs.reshape(n, -1)
        self._ys = ys.reshape(n, -1)
        self._zs = zs.reshape(n, -1)

        self._fwidth = self._ys[0, 1] - self._ys[0, 0]

        if len(tmp) > 3:
            partial_density = tmp[3:]
            ncol = len(partial_density)
            self._partial_density = partial_density.reshape(ncol, n, -1)
        else:
            self._partial_density = None

    def plot(self, ax):
        variables = self._variables

        self.create_list_symbol_indices()

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

        sf_min = variables["sf_min"]
        sf_max = variables["sf_max"]
        d_sf = variables["d_sf"]
        n_sf = int(sf_max / float(d_sf))
        ax.set_yticks(np.linspace(sf_min, sf_max, n_sf + 1))
        ax.set_ylabel("Spectral function (/{})".format(variables["freq_unit"]))
        ax.set_ylim(sf_min - d_sf * 0.25, sf_max)

        ax.axvline(0, color="k", dashes=(2, 2), linewidth=0.5)

        ax.axhline(0, color="k", dashes=(2, 2), linewidth=0.5)  # zero axis

        figure_name = self.create_figure_name()
        pdf = PdfPages(figure_name)
        for i, x in enumerate(self._xs):
            print(i)
            freqs = make_steplike(self._ys[i], self._fwidth)
            zs = make_steplike(self._zs[i], 0.0)
            lines = ax.plot(
                freqs * variables["unit"],
                zs,
                color=variables["linecolor"],
                dashes=variables["dashes"],
                label="Total",
            )
            lines_symbols = self.plot_symbol(ax, i)
            ax.legend(loc=2, framealpha=0.5)
            pdf.savefig(dpi=288, transparent=True)
            lines[0].remove()
            for lines in lines_symbols:
                lines[0].remove()
        pdf.close()

    def plot_symbol(self, ax, iq):
        variables = self._variables
        lines_symbols = []
        colors = ("#ff0000", "#0000ff", "#007f00")
        tuple_dashes = ((2, 2), (1, 1), (2, 1))
        for i, symbol_indices in enumerate(self._list_symbol_indices):
            s, indices = symbol_indices
            freqs = make_steplike(self._ys[iq], self._fwidth)
            spectral_function = np.sum(self._partial_density[indices, iq], axis=0)
            spectral_function = make_steplike(spectral_function, 0.0)
            lines = ax.plot(
                freqs * variables["unit"],
                spectral_function,
                color=colors[i],
                dashes=tuple_dashes[i],
                label=s,
            )
            lines_symbols.append(lines)
        return lines_symbols

    def create_list_symbol_indices(self):
        from phonopy.interface.vasp import read_vasp
        print(self._variables)
        filename = self._variables["poscar"]
        symbols = read_vasp(filename).get_chemical_symbols()
        symbols3 = [s for s in symbols for i in range(3)]
        reduced_symbols = sorted(set(symbols), key=symbols.index)
        list_symbol_indices = []
        for s in reduced_symbols:
            indices = [i for i, x in enumerate(symbols3) if x == s]
            list_symbol_indices.append((s, indices))
        self._list_symbol_indices = list_symbol_indices
        print("list_symbol_indices:")
        print(list_symbol_indices)

    def create_figure_name(self):
        variables = self._variables
        figure_name = "spectral_functions_{}.{}".format(
            variables["freq_unit"],
            variables["figure_type"])
        return figure_name

    def save_figure(self, fig, figure_name):
        pass

def make_steplike(values, width):
    """
    Args:
        values: 1D array
    """
    return np.vstack((values - width * 0.5, values + width * 0.5)).T.flatten()
