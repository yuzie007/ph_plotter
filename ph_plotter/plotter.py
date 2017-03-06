#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import os
from cycler import cycler
import numpy as np
import matplotlib.pyplot as plt


__author__ = "Yuji Ikeda"


def update_prop_cycle(linewidth):
    # https://github.com/vega/vega/wiki/Scales#scale-range-literals
    colors = [
        '#1f77b4',
        '#ff7f0e',
        '#2ca02c',
        '#d62728',
        '#9467bd',
        '#8c564b',
        '#e377c2',
        '#7f7f7f',
        '#bcbd22',
        '#17becf',
    ] * 3
    dashes_list = [
        (4, 1),
        (2, 1),
        (4, 1, 2, 1),
        (4, 1, 2, 1, 2, 1),
        (4, 1, 2, 1, 2, 1, 2, 1),
        (8, 1, 4, 1),
    ] * 5
    for i, dashes in enumerate(dashes_list):
        dashes_list[i] = _modify_dashes_by_linewidth(dashes, linewidth)

    plt.rc('axes', prop_cycle=cycler('color', colors) + cycler('dashes', dashes_list))


def _modify_dashes_by_linewidth(dashes, linewidth):
    return tuple(np.array(dashes) * linewidth)


def read_primitive_matrix(phonopy_conf):
    from phonopy.cui.settings import PhonopyConfParser

    settings = PhonopyConfParser(phonopy_conf, option_list=[]).get_settings()
    return settings.get_primitive_matrix()


def read_band_labels(phonopy_conf):
    from phonopy.cui.settings import PhonopyConfParser

    settings = PhonopyConfParser(phonopy_conf, option_list=[]).get_settings()
    band_labels = settings.get_band_labels()
    gamma_str = r"\Gamma"
    if band_labels is not None:
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

    def _create_default_variables(self):
        self._variables = {
            "freq_unit": "THz",
            "unit": 1.0,
            "f_min": -2.0,
            "f_max": 10.0,
            "d_freq": 2.0,
            "dos_min": 0.0,
            "dos_max": 0.4,
            "dos_ticks": 0.1,
            "sf_min": 0.0,
            "sf_max": 2.0,
            "d_sf": 0.5,
            "figure_type": "pdf",
            "figsize": (5.0, 3.5),
            "fontsize": 12.0,
            "linecolor": "k",
            "linewidth": 1,
            "dashes": (),
            "colormap_p": "r",
            "colormap_n": "w",
            "alpha": 1.0,
            "is_transparent_gradient": False,
            "markersize": 5.0,
            "poscar": "POSCAR",
            "sf_with": "atoms",
            "ninterp": None,
            "selected_irreps": None,
            "combinations_elements": None,
        }

    def update_variables(self, variables):
        for k, v in variables.items():
            if v is not None:
                self._variables[k] = v

    def load_data(self):
        raise NotImplementedError

    def configure(self, ax):
        raise NotImplementedError

    def plot(self, ax):
        raise NotImplementedError

    def create_figure_name(self):
        raise NotImplementedError

    def create_figure(self):
        variables = self._variables

        fontsize = variables['fontsize']
        params = {
            "font.family": "Arial",
            "font.size": fontsize,
            # "mathtext.fontset": "custom",
            # "mathtext.it": "Arial",
            "mathtext.default": "regular",
            "legend.fontsize": fontsize,
        }
        plt.rcParams.update(params)
        update_prop_cycle(variables['linewidth'])  # This may be not needed for matplotlib 2.x

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

        from scipy.constants import eV, Planck
        THz2meV = Planck / eV * 1e+15  # 4.135667662340164

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

    def create_primitive(self, filename="POSCAR", conf_file=None):
        from phonopy.structure.cells import get_primitive
        from phonopy.interface.vasp import read_vasp
        if conf_file is None:
            self._check_conf_files()
        else:
            self.set_conf_file(conf_file)
        primitive_matrix = self._read_primitive_matrix()
        atoms = read_vasp(filename)
        return get_primitive(atoms, primitive_matrix)

    def _read_primitive_matrix(self):
        from phonopy.cui.settings import PhonopyConfParser
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
                self.set_conf_file(conf_file)
                return

    def set_conf_file(self, conf_file):
        self._conf_file = conf_file

    def get_object_plotted(self):
        return self._object_plotted
