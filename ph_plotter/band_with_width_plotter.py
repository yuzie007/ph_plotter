#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import h5py
import numpy as np
from .band_plotter import BandPlotter
from .plotter import read_band_labels
from ph_unfolder.irreps.irreps import extract_degeneracy_from_ir_label

__author__ = 'Yuji Ikeda'


# TODO(ikeda): Sort also ir_labels
class BandWithWidthPlotter(BandPlotter):
    def load_data(self, data_file="sf_fit.hdf5"):
        print("Reading data_file: ", end="")
        with h5py.File(data_file, 'r') as data:
            self._paths = np.array(data['paths'])
            npaths, npoints = self._paths.shape[:2]

            self._is_squared = np.array(data['is_squared'])

            keys = [
                'natoms_primitive',
                'elements',
                'distance',
                'pointgroup_symbol',
                'num_irreps',
                'ir_labels',
            ]
            data_points = []
            distances = []
            frequencies = []
            widths = []
            fiterrs = []
            for ipath in range(npaths):
                distances_on_path = []
                frequencies_on_path = []
                widths_on_path = []
                fiterrs_on_path = []
                for ip in range(npoints):
                    group_name = '{}/{}/'.format(ipath, ip)
                    group = data[group_name]
                    data_points.append(
                        {k: group[k][...] for k in keys}
                    )

                    distances_on_path.append(group['distance'][...])

                    indices_nonzero = np.where(np.isfinite(group['norms_s']))

                    frequencies_on_point = []
                    widths_on_point = []
                    fiterrs_on_point = []
                    for index in indices_nonzero[0]:
                        ir_label = str(group['ir_labels'][index], encoding='ascii')
                        degeneracy = extract_degeneracy_from_ir_label(ir_label)
                        for i in range(degeneracy):
                            frequencies_on_point.append(group['peaks_s' ][index])
                            widths_on_point     .append(group['widths_s'][index])
                            fiterrs_on_point.append(group['fitting_errors'][index])

                    frequencies_on_point = np.asarray(frequencies_on_point)
                    widths_on_point      = np.asarray(widths_on_point)
                    fiterrs_on_point     = np.asarray(fiterrs_on_point)

                    indices_sort = np.argsort(frequencies_on_point)
                    # print(indices_sort, frequencies_on_point)

                    frequencies_on_path.append(frequencies_on_point[indices_sort])
                    widths_on_path     .append(widths_on_point     [indices_sort])
                    fiterrs_on_path    .append(fiterrs_on_point    [indices_sort])

                distances.append(distances_on_path)
                frequencies.append(frequencies_on_path)
                widths.append(widths_on_path)
                fiterrs.append(fiterrs_on_path)
        print("Finished")

        distances   = np.array(distances)
        widths      = np.array(widths)

        self._data_points = data_points

        self._distances = distances / distances[-1, -1]
        self._frequencies = np.asarray(frequencies)
        self._bandwidths = widths
        self._fiterrs = np.asarray(fiterrs)

        band_labels = read_band_labels("band.conf")
        print("band_labels:", band_labels)
        self._band_labels = band_labels

        return self

    def plot(self, ax):
        variables = self._variables
        distances = self._distances
        frequencies = self._frequencies
        bandwidths = self._bandwidths

        npath, nqpoint, nband = frequencies.shape
        for ipath in range(npath):
            lines = ax.plot(
                distances[ipath],
                frequencies[ipath] * variables["unit"],
                variables["linecolor"],
                dashes=variables["dashes"],
                linewidth=variables["linewidth"],
            )
            for ib in range(nband):
                ax.fill_between(
                    distances[ipath],
                    (frequencies[ipath, :, ib] + bandwidths[ipath, :, ib]) * variables["unit"],
                    (frequencies[ipath, :, ib] - bandwidths[ipath, :, ib]) * variables["unit"],
                    edgecolor="none",
                    facecolor=variables['linecolor'],
                    alpha=variables['alpha'],
                )

    def plot_selected_curve(self, ax, ipath, ib):
        variables = self._variables
        distances = self._distances
        frequencies = self._frequencies
        bandwidths = self._bandwidths

        npath, nqpoint, nband = frequencies.shape
        lines = ax.plot(
            distances[ipath],
            frequencies[ipath, :, ib] * variables["unit"],
            variables["linecolor"],
            dashes=variables["dashes"],
            linewidth=variables["linewidth"],
        )
        ax.fill_between(
            distances[ipath],
            (frequencies[ipath, :, ib] + bandwidths[ipath, :, ib]) * variables["unit"],
            (frequencies[ipath, :, ib] - bandwidths[ipath, :, ib]) * variables["unit"],
            edgecolor="none",
            facecolor=variables['linecolor'],
            alpha=variables['alpha'],
        )

    def create_figure_name(self):
        variables = self._variables
        figure_name = "band_{}.{}".format(
            variables["freq_unit"],
            variables["figure_type"])
        return figure_name
