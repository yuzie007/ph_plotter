#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import os
import numpy as np
from ph_plotter.plotter import Plotter
from ph_plotter.file_io import read_band_hdf5_dict


class SFPlotter(Plotter):
    def __init__(
            self,
            variables=None,
            is_horizontal=False,
            is_separated=False):
        super(SFPlotter, self).__init__(variables, is_horizontal)

        if is_separated:
            tmp_func = self.load_spectral_functions_multiple
        else:
            tmp_func = self.load_spectral_functions_single
        self.load_spectral_functions = tmp_func

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
        if "nums_arms" in data:
            self._nums_arms = data["nums_arms"]
        if "rot_pr_weights" in data:
            self._rot_pr_weights = data["rot_pr_weights"]
        if "pg_symbols" in data:
            self._pg_symbols = data["pg_symbols"].reshape(nq)
        if "nums_irreps" in data:
            self._nums_irreps = data["nums_irreps"].reshape(nq)
        if "ir_labels" in data:
            self._ir_labels = data["ir_labels"].reshape(nq, -1)
        if "natoms_primitive" in data:
            self._natoms_primitive = data["natoms_primitive"]
        if "elements" in data:
            self._elements = data["elements"]

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
            self._partial_sf = partial_density.reshape(ncol, n, -1)
        else:
            self._partial_sf = None

    def load_spectral_functions_single(
            self,
            filename="spectral_functions.dat",
            npath=None,
            nqp=None):
        import pandas as pd

        nq = npath * nqp

        tmp = pd.read_table(
            filename, delim_whitespace=True, header=None, comment="#")
        tmp = tmp.as_matrix().T
        xs = tmp[0]
        ys = tmp[1]
        total_sf = tmp[2]

        self._xs = xs.reshape(nq, -1) / np.nanmax(xs)
        self._ys = ys.reshape(nq, -1)
        self._total_sf = total_sf.reshape(nq, -1)

        if len(tmp) > 3:
            partial_sf = tmp[3:]
            ncol = len(partial_sf)
            self._partial_sf = partial_sf.reshape(ncol, nq, -1)
        else:
            self._partial_sf = None

        self._zs = self._total_sf

    def load_spectral_functions_multiple(
            self,
            filename="spectral_functions.dat",
            npath=None,
            nqp=None):
        import pandas as pd
        from ph_unfolder.irreps.character_tables import character_tables

        def modify_partial_sf_q(partial_sf_q):
            max_irs = 12
            ipad = max_irs - len(partial_sf_q)  # Needed to be filled
            partial_sf_q = np.pad(
                partial_sf_q,
                ((0, ipad), (0, 0)),
                mode=b'constant',
                constant_values=np.nan)
            return partial_sf_q

        dirname, basename = os.path.split(filename)
        if dirname == '':
            dirname = '.'
        dirname += '/'

        xs = []
        ys = []
        total_sf = []
        partial_sf = []
        pg_symbols = []
        ir_labels = []
        num_irs = []
        for ipath in range(npath):
            for iqp in range(nqp):
                tmp_dir = "{}_{}/".format(ipath, iqp)
                print(tmp_dir)
                new_filename = dirname + tmp_dir + basename
                tmp = pd.read_table(
                    new_filename,
                    delim_whitespace=True,
                    header=None)
                tmp = tmp.as_matrix().T
                xs.append(tmp[0])
                ys.append(tmp[1])
                total_sf.append(tmp[2])
                if len(tmp) > 3:
                    partial_sf.append(modify_partial_sf_q(tmp[3:]))

                with open(dirname + tmp_dir + "pointgroup_symbol", "r") as f:
                    for line in f:
                        pg_symbol = line.strip()
                pg_symbols.append(pg_symbol)
                ir_label_list = character_tables[pg_symbol]["ir_labels"]
                ir_labels.append(ir_label_list)
                num_irs.append(len(ir_label_list))

        xs = np.array(xs)

        self._xs = xs / np.nanmax(xs)
        self._ys = np.array(ys)
        self._total_sf = np.array(total_sf)

        self._pg_symbols = np.array(pg_symbols)
        self._ir_labels = pd.DataFrame(ir_labels).as_matrix()
        self._nums_irreps = np.array(num_irs)

        if len(partial_sf) != 0:
            partial_sf = np.array(partial_sf)
            self._partial_sf = partial_sf.transpose((1, 0, 2))
        else:
            self._partial_sf = None

        self._zs = self._total_sf
