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
from scipy.interpolate import RegularGridInterpolator as RGI


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

        X, Y = np.meshgrid(self.xs, self.ys)
        self.points = np.stack([X.flatten(), Y.flatten()]).T
        self.valeurs = np.zeros((Nt, Nx, Ny))

    def initialisation_terminale(self):
        """Initialisation de la fonction valeur en fonction du cout terminal.
        """
        self.indice = len(self.ts) - 1
        self.valeurs[-1, ...] = ((self.xs[:, np.newaxis]) ** 2
                                 + (self.ys[np.newaxis, :] - self.sys.by) ** 2
                                 ) / 2.

    def step(self):
        f_libre = self.sys.flux_libre(self.points)
        p_libre = self.points + self.dt * f_libre

        f_bang = self.sys.flux_bang(self.points)
        p_bang = self.points + self.dt + f_bang

        self.indice -= 1
        approx = RGI((self.xs, self.ys), self.valeurs[self.indice + 1, ...])
        self.valeurs[self.indice] = np.minimum(approx(p_libre), approx(p_bang))
