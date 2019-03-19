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
    """Evolution de la fonction valeur pour un système contrôlé donné et
    sur une grille donnée.

    :param sys: Sytème différentiel associé.
    :type sys: Systeme
    :param xs: grille spatiale en x
    :type xs: numpy.ndarray
    :param ys: grille spatiale en y
    :type ys: numpy.ndarray
    :param ts: grille temporelle
    :type ts: numpy.ndarray
    """
    def __init__(self, sys, xs, ys, ts):
        self.sys = sys
        self.xs = xs
        self.ys = ys
        self.ts = ts

        X, Y = np.meshgrid(self.xs, self.ys)
        self.points = np.stack([X.T.flatten(), Y.T.flatten()]).T
        self.valeurs = np.zeros((len(ts), len(xs), len(ys)))

    @classmethod
    def from_dl(cls, sys, T, dl):
        """Constructeur alternatif simplifié. Garanti la condition CFL.

        :param sys: système différentiel
        :type sys: Systeme
        :param T: fenetre de temps pour l'action du contrôle
        :type T: float
        :param dl: taille de la discrétisation spatiale
        :type dl: float
        """
        Nx = math.floor(sys.bx / dl)
        xs = np.linspace(0, sys.bx, Nx)

        Ny = math.floor(sys.by / dl)
        ys = np.linspace(0, sys.by, Ny)

        Nt = math.ceil(math.sqrt(2) * T * sys.borne() / dl)
        ts = np.linspace(0, T, Nt)
        return cls(sys=sys, xs=xs, ys=ys, ts=ts)

    def verification_cfl(self):
        """Test la condifion CFL."""
        dx = (self.xs[-1] - self.xs[0]) / len(self.xs)
        dy = (self.ys[-1] - self.ys[0]) / len(self.ys)
        dl = min(dx, dy)
        dt = (self.ts[-1] - self.ts[0]) / len(self.ts)
        return np.sqrt(2) * dt * self.sys.borne() <= dl

    def verification_extremites(self):
        """Vérification que la grille spatiale va jusqu'au état semitriviaux.
        """
        return (self.xs[-1] == self.sys.bx) and (self.ys[-1] == self.sys.by)

    def initialisation_terminale(self):
        """Initialisation de la fonction valeur en fonction du cout terminal.
        """
        self.valeurs[-1, ...] = (np.abs(self.xs[:, np.newaxis])
                                 + np.abs(1. - self.ys[np.newaxis, :]))

    def nouveaux_points(self, dt):
        """Récupération des points après déplacement par les flux.

        :param dt: pas de temps
        :type dt: float
        """
        f_libre = self.sys.flux_libre(self.points)
        p_libre = self.points + dt * f_libre

        f_bang = self.sys.flux_bang(self.points)
        p_bang = self.points + dt * f_bang
        return p_libre, p_bang

    def step(self, vals, dt):
        """Passage de l'instant t à t - delta_t, contrôle supposé bang-bang.

        :param vals: Tableau des valeurs
        :type vals: numpy.array (len(self.xs), len(self.ys))
        :param dt: pas de temps
        :type dt: float
        """
        p_libre, p_bang = self.nouveaux_points(dt)
        approx = RGI((self.xs, self.ys), vals)
        v_libre = approx(p_libre)
        v_bang = approx(p_bang)
        return np.minimum(v_libre, v_bang).reshape(len(self.xs), len(self.ys))

    def resolution(self):
        """Resolution de l'équation d'Hamilton-Jacobi pour la fonction valeur.
        """
        self.initialisation_terminale()
        for k in reversed(range(1, len(self.ts))):
            self.valeurs[k - 1] = (self.step(vals=self.valeurs[k],
                                   dt=self.ts[k] - self.ts[k - 1]))
