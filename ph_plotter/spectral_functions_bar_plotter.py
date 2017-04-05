#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import numpy as np
from matplotlib.ticker import AutoMinorLocator
from matplotlib.backends.backend_pdf import PdfPages
from ph_plotter.points_sf_plotter import PointsSFPlotter
from ph_plotter.file_io import read_band_hdf5_dict


__author__ = "Yuji Ikeda"


class SpectralFunctionsPlotter(PointsSFPlotter):
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

        self.create_list_element_indices()
        # For back-compatibility
        if self._partial_density.shape[0] == 3 * self._natoms:
            self._expand_list_element_indices()
        print("list_element_indices:")
        print(self._list_element_indices)

        return self

    def _create_sf_filename(self, data_file):
        sf_filename = data_file.replace(
            "band.hdf5", "spectral_functions_atoms.dat")
        return sf_filename

    def plot(self, ax):
        self._fwidth = self._ys[0, 1] - self._ys[0, 0]
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
        lines_symbols = self.plot_elements_q(ax, iq)
        return lines_total, lines_symbols

    def plot_total_q(self, ax, iq):
        variables = self._variables

        freqs = make_steplike(self._ys[iq], self._fwidth)
        sf = make_steplike(self._zs[iq], 0.0)

        if self._is_horizontal:
            xs = freqs * variables["unit"]
            ys = sf
        else:
            xs = sf
            ys = freqs * variables["unit"]

        lines_total = ax.plot(
            xs,
            ys,
            color=variables["linecolor"],
            dashes=variables["dashes"],
            linewidth=variables["linewidth"],
            label="Total",
        )

        return lines_total

    def plot_elements_q(self, ax, iq):

        for counter, element_indices in enumerate(self._list_element_indices):
            element_label, indices = element_indices
            sf_symbol = np.sum(self._partial_density[indices, iq], axis=0)
            sf_symbol = make_steplike(sf_symbol, 0.0)

            self._plot_curve(ax, iq, sf_symbol, label=element_label)

        return

    def create_list_element_indices(self):
        from phonopy.interface.vasp import read_vasp
        filename = self._variables["poscar"]
        atoms = read_vasp(filename)

        symbols = atoms.get_chemical_symbols()
        reduced_symbols = sorted(set(symbols), key=symbols.index)
        list_element_indices = []
        for s in reduced_symbols:
            indices = [i for i, x in enumerate(symbols) if x == s]
            list_element_indices.append((s, indices))

        self._natoms = atoms.get_number_of_atoms()
        self._list_element_indices = list_element_indices

    def create_figure_name(self):
        variables = self._variables
        figure_name = "spectral_functions_elements_{}.{}".format(
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
