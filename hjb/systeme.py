#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 perrollaz <perrollaz@vincent-MacBookPro>
#
# Distributed under terms of the MIT license.

"""
Cartographie d'un système de Lotka-Volterra compétitif à deux
espèces avec un contrôle multiplicatif de prélevement.

.. math::
    \\begin{equation}
        \\begin{cases}
            \\dot{x} = x (a (\\bar{x} - x) - b y) - \\alpha x u\\\\
            \\dot{y} = y (d (\\bar{y} - y) - c x) - \\beta y u
        \\end{cases}
    \\end{equation}
"""
import numpy as np


class Systeme:
    """Modélisation d'un flux pour le système de Lotka-Volterra ci dessus."""
    def __init__(self, a, b, c, d, alpha, beta, M, bx, by):
        self._a = a
        self._b = b
        self._c = c
        self._d = d
        self.bx = bx
        self.by = by
        self._alpha = alpha
        self._beta = beta
        self._M = M

    @classmethod
    def exemple_simple(cls):
        return cls(a=1, b=1, c=1, d=1, alpha=1, beta=1, M=1, bx=1, by=1)

    @classmethod
    def exemple_bistable(cls):
        return cls(a=1, b=2, c=2, d=1, alpha=1, beta=1, M=1, bx=1, by=1)

    def _parametres_positifs(self):
        """Vérification que les arguments sont positifs."""
        for attribut in vars(self):
            if getattr(self, attribut) < 0:
                return False
        return True

    def _regime_bistable(self):
        """Vérification du régime bistable."""
        x_stable = (self._d * self.by - self._c * self.bx < 0)
        y_stable = (self._a * self.bx - self._b * self.by < 0)
        return x_stable and y_stable

    def verifications(self):
        """Ensemble des vérifications: positivité, bistabilité, coexistence."""
        pos = self._parametres_positifs()
        bis = self._regime_bistable()
        det = self._a * self._d - self._b * self._c < 0
        return pos and bis and det

    def etat_coexistence(self):
        """Calcul de l'état d'équilibre de coexistence des espèces."""
        det = self._a * self._d - self._b * self._c
        return (self._d * (self._a * self.bx - self._b * self.by) / det,
                self._a * (self._d * self.by - self._c * self.bx) / det)

    def __repr__(self):
        arguments = ["a", "b", "c", "d", "alpha", "beta", "M"]
        correspondance = {arg: getattr(self, f"_{arg}")
                          for arg in arguments}
        arguments = ", ".join([a+"={}".format(correspondance[a])
                               for a in arguments])
        autres = ", bx={}, by={}".format(self.bx, self.by)
        return "Systeme({})".format(arguments + autres)

    def flux(self, X, u):
        """Evaluation du flux pour l'état X et le contrôle u.

        :param X: état du système
        :type X: numpy.array (n,2)
        :param u: contrôle
        :type u: numpy.array (n)
        """
        assert np.alltrue((0 <= u) & (u <= self._M))
        x, y = X[..., 0], X[..., 1]
        return np.stack([x * (self._a * (self.bx - x) - self._b * y
                         - self._alpha * u),
                         y * (self._d * (self.by - y) - self._c * x
                         - self._beta * u)]).T

    def flux_libre(self, X):
        """Flux sans contrôle.

        :param X: état du système
        :type X: 2-tuple ou numpy.array
        """
        return self.flux(X, 0.)

    def flux_bang(self, X):
        """Flux avec contrôle saturé.

        :param X: état du système
        :type X: 2-tuple ou numpy.array
        """
        return self.flux(X, self._M)

    def borne(self):
        """Renvoit un majorant brut de la norme du flux dans le carré stable.
        """
        arr = np.array([self.bx * (self._a * self.bx + self._b * self.by
                                   + self._alpha * self._M),
                        self.by * (self._c * self.bx + self._d * self.by
                                   + self._beta * self._M)])
        return np.linalg.norm(arr)

    def dessin(self, ax):
        """Dessine les points d'équilibres et les isoclines dans le repère.

        :param ax: repère
        :type ax: pyplot.Axes
        """
        xe, ye = self.etat_coexistence()
        ax.scatter([0, self.bx, 0, xe], [0, 0, self.by, ye], color="red")
        ax.plot([0, self.bx, 0],
                [0, 0, self._a * self.by / self._b],
                color="blue")
        ax.plot([0, 0, self._d * self.by / self._c],
                [0, self.by, 0],
                color="yellow")
