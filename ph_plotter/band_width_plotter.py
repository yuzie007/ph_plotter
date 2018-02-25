#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import h5py
import numpy as np
from matplotlib.ticker import AutoMinorLocator
from .band_plotter import BandPlotter
from .plotter import read_band_labels
from .colormap_creator import ColormapCreator

from ph_unfolder.irreps.irreps import extract_degeneracy_from_ir_label

__author__ = 'Yuji Ikeda'


class FitPointLoader(object):
    def __init__(self, data, is_sorted):
        self._load(data)
        if is_sorted:
            self._sort_data()

    def _load(self, data):
        indices_nonzero = np.where(np.isfinite(data['norms_s']))

        frequencies = []
        widths = []
        fiterrs = []
        ir_labels = []
        for index in indices_nonzero[0]:
            ir_label = str(data['ir_labels'][index], encoding='ascii')
            degeneracy = extract_degeneracy_from_ir_label(ir_label)
            for i in range(degeneracy):
                frequencies.append(data['peaks_s'][index])
                widths     .append(data['widths_s'][index])
                fiterrs    .append(data['fitting_errors'][index])
                ir_labels  .append(ir_label)

        self._distance = data['distance'][...]
        self._frequencies = np.asarray(frequencies)
        self._widths      = np.asarray(widths)
        self._fiterrs     = np.asarray(fiterrs)
        self._ir_labels   = np.asarray(ir_labels)

    def _sort_data(self):
        indices = np.argsort(self._frequencies)

        self._frequencies = self._frequencies[indices]
        self._widths      = self._widths     [indices]
        self._fiterrs     = self._fiterrs    [indices]
        self._ir_labels   = self._ir_labels  [indices]

    def get_distance(self):
        return self._distance

    def get_frequencies(self):
        return self._frequencies

    def get_widths(self):
        return self._widths

    def get_fiterrs(self):
        return self._fiterrs

    def get_ir_labels(self):
        return self._ir_labels


# TODO(ikeda): Sort also ir_labels
class BandWidthPlotter(BandPlotter):
    def __init__(self, *args, **kwargs):
        super(BandWidthPlotter, self).__init__(*args, **kwargs)
        self._set_is_sorted()

    def _set_is_sorted(self):
        self._is_sorted = True

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
            ir_labels = []
            for ipath in range(npaths):
                distances_on_path = []
                for ip in range(npoints):
                    group_name = '{}/{}/'.format(ipath, ip)
                    group = data[group_name]
                    data_points.append(
                        {k: group[k][...] for k in keys}
                    )

                    fit_point_loader = FitPointLoader(group, self._is_sorted)

                    distances_on_path.append(fit_point_loader.get_distance())
                    frequencies_on_point = fit_point_loader.get_frequencies()
                    widths_on_point      = fit_point_loader.get_widths()
                    fiterrs_on_point     = fit_point_loader.get_fiterrs()
                    ir_labels_on_point   = fit_point_loader.get_ir_labels()

                    frequencies.append(frequencies_on_point)
                    widths.append(widths_on_point)
                    fiterrs.append(fiterrs_on_point)
                    ir_labels.append(ir_labels_on_point)

                distances.append(distances_on_path)

        print("Finished")


        self._data_points = data_points

        distances = np.array(distances)
        self._distances = distances / distances[-1, -1]
        self._frequencies = np.asarray(frequencies)
        self._bandwidths = np.asarray(widths)
        self._fiterrs = np.asarray(fiterrs)
        self._ir_labels = np.asarray(ir_labels)

        band_labels = read_band_labels("band.conf")
        print("band_labels:", band_labels)
        self._band_labels = band_labels

        return self

    def plot(self, ax):
        variables = self._variables
        distances = self._distances
        frequencies = self._frequencies
        bandwidths = self._bandwidths

        nq, nband = frequencies.shape
        lines = ax.plot(
            distances.flatten(),
            frequencies * variables["unit"],
            variables["linecolor"],
            dashes=variables["dashes"],
            linewidth=variables["linewidth"],
            )
        for ib in range(nband):
            ax.fill_between(
                distances.flatten(),
                (frequencies[:, ib] + bandwidths[:, ib]) * variables["unit"],
                (frequencies[:, ib] - bandwidths[:, ib]) * variables["unit"],
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
        return "band_width.{}".format(self._variables["figure_type"])
