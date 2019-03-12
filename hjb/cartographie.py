#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 perrollaz <perrollaz@vincent-MacBookPro>
#
# Distributed under terms of the MIT license.

"""
Cartographie de la fonction valeur.
"""
import math
import numpy as np


class Valeur:
    """Evolution de la fonction valeur pour un système donné en un temps donné
    avec une certaine taille de grille.

    :param sys: Sytème différentiel associé.
    :type sys: Systeme
    :param T: Horizon de temps pour le contrôle.
    :type T: float
    :param dl: taille de la grille spatiale.
    """
    def __init__(self, sys, T, dl):
        self.sys = sys
        self.T = T
        self.dl = dl

        Nx = math.floor(sys.bx / dl)
        self.dx = sys.bx / Nx
        self.xs = np.linspace(0, sys.bx, Nx)

        Ny = math.floor(sys.by / dl)
        self.dy = sys.by / Ny
        self.ys = np.linspace(0, sys.by, Ny)

        Nt = math.ceil(math.sqrt(2) * T * sys.borne() / dl)
        self.dt = T / Nt
        self.ts = np.linspace(0, T, Nt)

        self.valeurs = np.zeros((Nt, Nx, Ny))

    def initialisation_terminale(self):
        self.valeurs[-1, ...] = ((self.xs[:, np.newaxis]) ** 2
                                 + (self.ys[np.newaxis, :] - self.sys.by) ** 2
                                 ) / 2.
