#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import os
import h5py
import numpy as np
from ph_plotter.plotter import Plotter
from ph_plotter.plotter import read_band_labels


__author__ = "Yuji Ikeda"


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

    def load_data(self, data_file='sf.hdf5'):
        with h5py.File(data_file, 'r') as data:
            self._paths = np.array(data['paths'])
            npaths, npoints = self._paths.shape[:2]

            frequencies = np.array(data['frequencies'])
            self._is_squared = np.array(data['is_squared'])

            keys = [
                'natoms_primitive',
                'elements',
                'distance',
                'pointgroup_symbol',
                'num_irreps',
                'ir_labels',

                'total_sf',
                'partial_sf_s',
                'partial_sf_e',
                'partial_sf_s_e',
                'partial_sf_e2',
            ]
            data_points = []
            distances = []
            for ipath in range(npaths):
                distances_on_path = []
                for ip in range(npoints):
                    group = '{}/{}/'.format(ipath, ip)
                    data_points.append(
                        {k: np.array(data[group + k]) for k in keys if group + k in data}
                    )

                    distances_on_path.append(
                        np.array(data[group + 'distance']))
                distances.append(distances_on_path)

            self._data_points = data_points
            self._distances = np.array(distances)

        xs = self._distances.reshape(-1) / np.nanmax(self._distances)
        self._frequencies, self._xs = np.meshgrid(frequencies, xs)

        print("Finished")

        band_labels = read_band_labels("band.conf")
        print("band_labels:", band_labels)
        self._band_labels = band_labels

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
        self._frequencies = ys.reshape(nq, -1)
        self._total_sf = total_sf.reshape(nq, -1)

        if len(tmp) > 3:
            partial_sf = tmp[3:]
            ncol = len(partial_sf)
            self._partial_sf = partial_sf.reshape(ncol, nq, -1)
        else:
            self._partial_sf = None

        self._zs = self._total_sf

        self._is_squared = self._check_is_squared(filename)

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
        self._frequencies = np.array(ys)
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

    @staticmethod
    def _check_is_squared(filename):
        is_squared = True
        with open(filename, 'r') as f:
            for line in f:
                if 'is_squared' in line:
                    if line.split()[-1] == 'False':
                        is_squared = False
                    elif line.split()[-1] == 'True':
                        is_squared = True
                    break
        return is_squared

    def _create_sf_label(self):
        freq_unit = self._variables['freq_unit']
        if self._is_squared:
            superscript = '$^{\minus2}$'
        else:
            superscript = '$^{\minus1}$'
        sf_label = r'Spectral function ({}{})'.format(freq_unit, superscript)
        return sf_label

    def create_total_sf(self):
        total_sf = []
        for i, data_point in enumerate(self._data_points):
            total_sf.append(data_point['total_sf'])
        return np.array(total_sf)

    def get_data_points(self):
        return self._data_points

    def set_data_points(self, data_points):
        self._data_points = data_points
