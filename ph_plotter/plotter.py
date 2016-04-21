#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import os
import matplotlib.pyplot as plt
from units import THz2meV


def read_primitive_matrix(phonopy_conf):
    from phonopy.cui.settings import PhonopyConfParser

    settings = PhonopyConfParser(phonopy_conf, option_list=[]).get_settings()
    return settings.get_primitive_matrix()


def read_band_labels(phonopy_conf):
    from phonopy.cui.settings import PhonopyConfParser

    settings = PhonopyConfParser(phonopy_conf, option_list=[]).get_settings()
    band_labels = settings.get_band_labels()
    gamma_str = r"\Gamma"
    for i, band_label in enumerate(band_labels):
        band_labels[i] = band_label.replace(gamma_str, u"Γ")
    band_labels = tuple(band_labels)
    return band_labels


class Plotter(object):
    def __init__(self, variables=None, is_horizontal=False):
        if variables is None:
            variables = {}
        self._create_default_variables()
        self.update_variables(variables)

        self._is_horizontal = is_horizontal
        self._plot_atom = True
        self._plot_symbol = True
        self._plot_total = True

    def _create_default_variables(self):
        self._variables = {
            "freq_unit": "THz",
            "unit": 1.0,
            "f_min": -2.5,
            "f_max": 10.0,
            "d_freq": 2.5,
            "dos_min": 0.0,
            "dos_max": 0.4,
            "dos_ticks": 0.1,
            "sf_min": 0.0,
            "sf_max": 2.0,
            "d_sf": 0.5,
            "figure_type": "pdf",
            "figsize": (5.0, 3.5),
            "linecolor": "#ff0000",
            "linewidth": 1,
            "dashes": (),
            "colormap": "red",
            "alpha": 1.0,
            "poscar": "POSCAR",
        }

    def update_variables(self, variables):
        self._variables.update(variables)

    def load_data(self):
        raise NotImplementedError

    def load_spectral_functions(self, filename="density.dat"):
        import pandas as pd
        tmp = pd.read_table(filename, delim_whitespace=True, header=None)
        tmp = tmp.as_matrix().T
        xs = tmp[0]
        ys = tmp[1]
        zs = tmp[2]
        n1, n2 = self._distances.shape
        n = n1 * n2
        self._xs = xs.reshape(n, -1)
        self._ys = ys.reshape(n, -1)
        self._zs = zs.reshape(n, -1)

        if len(tmp) > 3:
            partial_density = tmp[3:]
            ncol = len(partial_density)
            self._partial_density = partial_density.reshape(ncol, n, -1)
        else:
            self._partial_density = None

    def configure(self, ax):
        pass

    def plot(self, ax):
        raise NotImplementedError

    def create_figure_name(self):
        raise NotImplementedError

    def create_figure(self):
        variables = self._variables

        fontsize = 12
        params = {
            "font.family": "Arial",
            "font.size": fontsize,
            "mathtext.fontset": "custom",
            "mathtext.it": "Arial",
            "legend.fontsize": fontsize,
        }
        plt.rcParams.update(params)

        fig, ax = plt.subplots(
            1, 1,
            figsize=variables["figsize"],
            frameon=False,
            tight_layout=True)

        self.configure(ax)
        self.plot(ax)

        figure_name = self.create_figure_name()
        self.save_figure(fig, figure_name)
        plt.close()

    def save_figure(self, fig, figure_name):
        fig.savefig(figure_name, transparent=True)

    def run(self):

        variables = self._variables

        self.load_data(variables["data_file"])

        variables.update({
            "freq_unit": "THz",
            "unit": 1.0,
        })
        self.update_variables(variables)
        self.create_figure()

        return

        # meV
        variables.update({
            "freq_unit": "meV",
            "unit": THz2meV,
        })
        scale = 4.0
        variables["f_min"]  *= scale
        variables["f_max"]  *= scale
        variables["d_freq"] *= scale
        self.update_variables(variables)
        self.create_figure()

    def create_primitive(self, filename="POSCAR"):
        from phonopy.structure.cells import get_primitive
        from phonopy.interface.vasp import read_vasp
        primitive_matrix = self._read_primitive_matrix()
        atoms = read_vasp(filename)
        return get_primitive(atoms, primitive_matrix)

    def _read_primitive_matrix(self):
        from phonopy.cui.settings import PhonopyConfParser
        self._check_conf_files()
        phonopy_conf_parser = PhonopyConfParser(
            self._conf_file,
            option_list=[],
        )
        primitive_matrix = (
            phonopy_conf_parser.get_settings().get_primitive_matrix()
        )
        return primitive_matrix

    def _check_conf_files(self):
        conf_files = [
            "band.conf",
            "dos_smearing.conf",
            "dos_tetrahedron.conf",
            "partial_dos_smearing.conf",
            "partial_dos_tetrahedron.conf",
        ]
        for conf_file in conf_files:
            if os.path.isfile(conf_file):
                self._conf_file = conf_file
                return
