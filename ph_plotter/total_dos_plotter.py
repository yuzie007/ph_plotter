#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

from units import THz2meV
from .dos_plotter import DOSPlotter


class TotalDOSPlotter(DOSPlotter):
    def load_data(self, data_file='total_dos.dat'):
        super(TotalDOSPlotter, self).load_data(data_file)
        return self

    def run(self):

        variables = self._variables

        primitive = self.create_primitive()
        natoms = primitive.get_number_of_atoms()
        symbols = primitive.get_chemical_symbols()
        print("natoms:", natoms)
        print("symbols:", symbols)

        self.set_figure_name_prefix("total_dos")
        self.set_plot_symbol(False)
        self.set_plot_atom(False)
        self.load_data(variables["data_file"])

        variables.update({
            "freq_unit": "THz",
            "unit": 1.0,
            "natoms": natoms,
            "symbols": symbols,
        })
        self.update_variables(variables)
        # self.set_is_horizontal(True)
        # self.plot_dos()
        self.set_is_horizontal(False)
        self.create_figure()

        return

        # meV
        scale = 4.0
        variables.update({
            "freq_unit": "meV",
            "unit": THz2meV,
        })
        variables["f_min"]  *= scale
        variables["f_max"]  *= scale
        variables["d_freq"] *= scale
        variables["dos_min"]   /= scale
        variables["dos_max"]   /= scale
        variables["dos_ticks"] /= scale
        self.update_variables(variables)
        # self.set_is_horizontal(True)
        # self.plot_dos()
        self.set_is_horizontal(False)
        self.create_figure()
