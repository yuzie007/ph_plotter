#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import numpy as np
from matplotlib.ticker import AutoMinorLocator
from matplotlib.backends.backend_pdf import PdfPages
from ph_plotter.sf_plotter import SFPlotter


__author__ = "Yuji Ikeda"


class PointsSFPlotter(SFPlotter):
    def configure(self, ax):
        variables = self._variables

        freq_label = "Frequency ({})".format(variables["freq_unit"])
        d_freq = variables["d_freq"]
        f_min = variables["f_min"]
        f_max = variables["f_max"]
        n_freq = int(round((f_max - f_min) / d_freq)) + 1

        sf_label = self._create_sf_label()
        sf_min = variables["sf_min"]
        sf_max = variables["sf_max"]
        d_sf = variables["d_sf"]
        nticks_sf = int(round((sf_max - sf_min) / d_sf)) + 1

        mlx = AutoMinorLocator(2)
        ax.xaxis.set_minor_locator(mlx)
        mly = AutoMinorLocator(2)
        ax.yaxis.set_minor_locator(mly)

        # zero axis
        ax.axvline(0, color="#b0b0b0", linewidth=0.8)
        ax.axhline(0, color="#b0b0b0", linewidth=0.8)

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
                print(iq, self._data_points[iq]['pointgroup_symbol'])
                lines_total, lines_symbols = self.plot_q(ax, iq)
                ax.legend(framealpha=0.5)
                pdf.savefig(dpi=288, transparent=True)

                if lines_total is not None:
                    lines_total[0].remove()
                if lines_symbols is not None:
                    for lines in lines_symbols:
                        lines[0].remove()

    def plot_q(self, ax, iq):
        raise NotImplementedError

    def plot_total_q(self, ax, iq):
        variables = self._variables

        sf = self._data_points[iq]['total_sf']

        if self._is_horizontal:
            xs = self._ys[iq] * variables["unit"]
            ys = sf
        else:
            xs = sf
            ys = self._ys[iq] * variables["unit"]

        lines_total = ax.plot(
            xs,
            ys,
            color=variables["linecolor"],
            dashes=variables["dashes"],
            linewidth=variables["linewidth"],
            label="Total",
        )

        return lines_total

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

    def _expand_list_element_indices(self):
        list_element_indices = self._list_element_indices
        ndim = 3
        expanded_list_element_indices = []
        for element_indices in list_element_indices:
            s, indices = element_indices

            indices = np.repeat(indices, ndim)
            indices *= ndim
            for i in range(ndim):
                indices[i::ndim] += i

            expanded_list_element_indices.append((s, indices))

        self._list_element_indices = expanded_list_element_indices

    def save_figure(self, fig, figure_name):
        pass

    @staticmethod
    def _modify_dashes_by_linewidth(dashes, linewidth):
        return tuple(np.array(dashes) * linewidth)

    @staticmethod
    def _reset_prop_cycle(ax):
        # http://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_prop_cycle.html#matplotlib.axes.Axes.set_prop_cycle
        ax.set_prop_cycle(None)
