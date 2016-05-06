#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import numpy as np
from matplotlib.ticker import AutoMinorLocator
from matplotlib.backends.backend_pdf import PdfPages
from .plotter import Plotter, read_band_labels
from .file_io import read_band_hdf5_dict


class SpectralFunctionsPlotter(Plotter):
    def load_data(self, data_file="band.hdf5"):
        print("Reading band.hdf5: ", end="")
        data = read_band_hdf5_dict(data_file)
        print("Finished")

        self._distances   = data["distances"]
        self._frequencies = data["frequencies"]
        self._pr_weights  = data["pr_weights"]
        self._nstars      = data["nqstars"]

        n1, n2 = self._distances.shape

        if "rot_pr_weights" in data:
            self._rot_pr_weights = data["rot_pr_weights"]
        if "num_irs" in data:
            self._num_irs = data["num_irs"].reshape(n1 * n2, -1)
        if "ir_labels" in data:
            self._ir_labels = data["ir_labels"].reshape(n1 * n2, -1)

        sf_datafile = data_file.replace("band.hdf5", "spectral_functions.dat")
        self.load_spectral_functions(sf_datafile)

        return self

    def configure(self, ax):
        variables = self._variables

        self.create_list_symbol_indices()

        freq_label = "Frequency ({})".format(variables["freq_unit"])
        d_freq = variables["d_freq"]
        f_min = variables["f_min"]
        f_max = variables["f_max"]
        n_freq = int(round((f_max - f_min) / d_freq)) + 1

        sf_label = "Spectral function (/{})".format(variables["freq_unit"])
        sf_min = variables["sf_min"]
        sf_max = variables["sf_max"]
        d_sf = variables["d_sf"]
        nticks_sf = int(sf_max / float(d_sf)) + 1

        mlx = AutoMinorLocator(2)
        ax.xaxis.set_minor_locator(mlx)
        mly = AutoMinorLocator(2)
        ax.yaxis.set_minor_locator(mly)

        # zero axis
        ax.axvline(0, color="k", dashes=(2, 2), linewidth=0.5)
        ax.axhline(0, color="k", dashes=(2, 2), linewidth=0.5)

        if self._is_horizontal:

            ax.set_xticks(np.linspace(f_min, f_max, n_freq))
            ax.set_xlabel(freq_label)
            ax.set_xlim(f_min, f_max)

            ax.set_yticks(np.linspace(sf_min, sf_max, nticks_sf))
            ax.set_ylabel(sf_label)
            ax.set_ylim(sf_min, sf_max)

        else:

            ax.set_yticks(np.linspace(f_min, f_max, n_freq))
            ax.set_ylabel(freq_label)
            ax.set_ylim(f_min, f_max)

            ax.set_xticks(np.linspace(sf_min, sf_max, nticks_sf))
            ax.set_xlabel(sf_label)
            ax.set_xlim(sf_min, sf_max)

    def plot(self, ax):
        figure_name = self.create_figure_name()
        with PdfPages(figure_name) as pdf:
            for iq, x in enumerate(self._xs):
                print(iq)
                lines_total, lines_symbols = self.plot_q(ax, iq)
                ax.legend(framealpha=0.5)
                pdf.savefig(dpi=288, transparent=True)
                lines_total[0].remove()
                for lines in lines_symbols:
                    lines[0].remove()

    def plot_q(self, ax, iq):
        lines_total = self.plot_total_q(ax, iq)
        if self._variables["is_irs"]:
            lines_symbols = self.plot_irs_q(ax, iq)
        else:
            lines_symbols = self.plot_symbols_q(ax, iq)
        return lines_total, lines_symbols

    def plot_total_q(self, ax, iq):
        variables = self._variables
        if self._is_horizontal:
            lines_total = ax.plot(
                self._ys[iq] * variables["unit"],
                self._zs[iq],
                color=variables["linecolor"],
                dashes=variables["dashes"],
                linewidth=variables["linewidth"],
                label="Total",
            )
        else:
            lines_total = ax.plot(
                self._zs[iq],
                self._ys[iq] * variables["unit"],
                color=variables["linecolor"],
                dashes=variables["dashes"],
                linewidth=variables["linewidth"],
                label="Total",
            )
        return lines_total

    def plot_symbols_q(self, ax, iq):
        from .attributes import colors, tuple_dashes
        variables = self._variables
        lines_symbols = []
        for i, symbol_indices in enumerate(self._list_symbol_indices):
            s, indices = symbol_indices
            sf_symbol = np.sum(self._partial_density[indices, iq], axis=0)
            if self._is_horizontal:
                lines = ax.plot(
                    self._ys[iq] * variables["unit"],
                    sf_symbol,
                    color=colors[i],
                    dashes=tuple_dashes[i],
                    linewidth=variables["linewidth"],
                    label=s,
                )
            else:
                lines = ax.plot(
                    sf_symbol,
                    self._ys[iq] * variables["unit"],
                    color=colors[i],
                    dashes=tuple_dashes[i],
                    linewidth=variables["linewidth"],
                    label=s,
                )
            lines_symbols.append(lines)
        return lines_symbols

    def plot_irs_q(self, ax, iq):
        from .attributes import colors, tuple_dashes
        variables = self._variables
        lines_symbols = []
        indices = self._find_nonzero_irs(iq)
        for counter, index in enumerate(indices):
            ir_label = self._ir_labels[iq, index]
            sf_symbol = self._partial_density[index, iq]
            if self._is_horizontal:
                lines = ax.plot(
                    self._ys[iq] * variables["unit"],
                    sf_symbol,
                    color=colors[counter % len(colors)],
                    dashes=tuple_dashes[counter % len(tuple_dashes)],
                    linewidth=variables["linewidth"],
                    label=ir_label,
                )
            else:
                lines = ax.plot(
                    sf_symbol,
                    self._ys[iq] * variables["unit"],
                    color=colors[counter % len(colors)],
                    dashes=tuple_dashes[counter % len(tuple_dashes)],
                    linewidth=variables["linewidth"],
                    label=ir_label,
                )
            lines_symbols.append(lines)
        return lines_symbols

    def _find_nonzero_irs(self, iq, prec=1e-6):
        num_irs = self._num_irs[iq]
        indices = np.where(np.sum(self._partial_density[:num_irs, iq], axis=1) > prec)[0]
        print(np.sum(self._partial_density[:num_irs, iq], axis=1))
        print(indices)
        return indices

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
