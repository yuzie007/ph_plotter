#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.backends.backend_pdf import PdfPages
from .plotter import Plotter


class DOSPlotter(Plotter):
    def load_data(self, data_file):
        data = np.loadtxt(data_file).T
        print(np.sum(data[1]))
        self._frequencies = data[0]
        self._dos_list = data[1:]
        return self

    def plot(self, ax):
        self.prepare(ax)
        if self._plot_total:
            figure_name = self.create_figure_name()
            lines = self.plot_dos_total(ax)
            fig = ax.get_figure()
            self.save_figure_dos_total(fig, figure_name)
            lines[0].remove()
        if self._plot_symbol:
            self.plot_dos_symbol(ax)
        if self._plot_atom:
            self.plot_dos_atom(ax)

    def set_is_horizontal(self, is_horizontal):
        self._is_horizontal = is_horizontal

    def set_plot_atom(self, plot_atom):
        self._plot_atom = plot_atom

    def set_plot_symbol(self, plot_symbol):
        self._plot_symbol = plot_symbol

    def set_plot_total(self, plot_total):
        self._plot_total = plot_total

    def set_figure_name_prefix(self, figure_name_prefix):
        self._figure_name_prefix = figure_name_prefix

    def create_figure_name(self, is_atom=False, symbol=False):
        variables = self._variables
        figure_name = self._figure_name_prefix
        if self._is_horizontal:
            figure_name += "_h"
        else:
            figure_name += "_v"
        if symbol:
            figure_name += "_symbol_{}".format(symbol)
        if is_atom:
            figure_name += "_atom"
        figure_name += "_{}.{}".format(
            variables["freq_unit"],
            variables["figure_type"],
        )
        return figure_name

    def prepare(self, ax):
        variables = self._variables

        freq_label = "Frequency ({})".format(variables["freq_unit"])
        d_freq = variables["d_freq"]
        f_min = variables["f_min"]
        f_max = variables["f_max"]
        n_freq = round((f_max - f_min) / d_freq) + 1

        dos_label  = "Phonon DOS (/{})".format(variables["freq_unit"])
        dos_min   = variables["dos_min"]
        dos_max   = variables["dos_max"]
        dos_ticks = variables["dos_ticks"]
        # Add 1 to include end points
        nticks_dos = round((dos_max - dos_min) / dos_ticks) + 1

        mlx = AutoMinorLocator(2)
        ax.xaxis.set_minor_locator(mlx)
        mly = AutoMinorLocator(2)
        ax.yaxis.set_minor_locator(mly)

        ax.set_xticks(np.linspace(dos_min, dos_max, nticks_dos))
        ax.set_xlabel(dos_label)
        ax.set_xlim(dos_min, dos_max)

        ax.set_yticks(np.linspace(f_min, f_max, n_freq))
        ax.set_ylabel(freq_label)
        ax.set_ylim(f_min, f_max)

        ax.axhline(0, color="k", dashes=(2, 2), linewidth=0.5)  # zero axis

    def plot_dos_total(self, ax):
        variables = self._variables

        lines = ax.plot(
            np.sum(self._dos_list, axis=0) / (variables["unit"] * variables["natoms"] * 3),
            self._frequencies * variables["unit"],
            variables["linecolor"],
            dashes=variables["dashes"],
            linewidth=variables["linewidth"],
        )
        return lines

    def save_figure_dos_total(self, fig, figure_name):
        fig.savefig(figure_name, transparent=True)

    def save_figure(self, fig, figure_name):
        # Since so far DOSPlotter saves the figure at the same time as
        # plotting procedure, this should not do anything.
        pass

    def plot_dos_symbol(self, ax):
        variables = self._variables

        symbols = self._variables["symbols"]
        reduced_symbols = sorted(set(symbols), key=symbols.index)
        print(reduced_symbols)
        for i, s in enumerate(reduced_symbols):
            indices = [i for i, x in enumerate(symbols) if x == s]
            print(indices)
            lines = ax.plot(
                np.sum(self._dos_list[indices], axis=0) / (variables["unit"] * variables["natoms"] * 3),
                self._frequencies * variables["unit"],
                variables["linecolor"],
                dashes=variables["dashes"],
                linewidth=variables["linewidth"],
            )
            figure_name = self.create_figure_name(symbol=s)
            fig = ax.get_figure()
            fig.savefig(figure_name, transparent=True)
            lines[0].remove()

    def plot_dos_atom(self, ax):
        variables = self._variables

        figure_name = self.create_figure_name(is_atom=True)
        pdf = PdfPages(figure_name)
        for i, dos in enumerate(self._dos_list):
            print(i)
            lines = ax.plot(
                self._dos_list[i] / (variables["unit"] * variables["natoms"] * 3),
                self._frequencies * variables["unit"],
                variables["linecolor"],
                dashes=variables["dashes"],
                linewidth=variables["linewidth"],
            )
            pdf.savefig(transparent=True)
            lines[0].remove()
        pdf.close()
