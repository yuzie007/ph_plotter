#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import numpy as np


def read_band_yaml(yaml_file="band.yaml"):
    import yaml
    data = yaml.load(open(yaml_file, "r"))
    nqpoint = data['nqpoint']
    npath = data['npath']
    natom = data['natom']
    nband = natom * 3
    nsep = nqpoint // npath
    distance = np.zeros((npath, nsep))
    frequency = np.zeros((npath, nsep, nband))
    for ipath in range(npath):
        for isep in range(nsep):
            iq = ipath * nsep + isep
            distance[ipath, isep] = data['phonon'][iq]['distance']
            for iband in range(nband):
                frequency[ipath, isep, iband] = (
                    data['phonon'][iq]['band'][iband]['frequency'])
    return distance, frequency


def read_band_hdf5(hdf5_file="band.hdf5"):
    import h5py
    with h5py.File(hdf5_file, "r") as f:
        paths       = f["paths"]
        distances   = f["distances"]
        nqstars     = f["nqstars"]
        frequencies = f["frequencies"]
        pr_weights  = f["pr_weights"]

        paths       = np.array(paths)
        distances   = np.array(distances)
        nqstars     = np.array(nqstars)
        frequencies = np.array(frequencies)
        pr_weights  = np.array(pr_weights)

    return distances, frequencies, pr_weights, nqstars
