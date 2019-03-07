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


class Flux:
    """Modélisation d'un flux pour le système de Lotka-Volterra ci dessus."""
    def __init__(self, a, b, c, d, bx, by, alpha, beta, M):
        self._a = a
        self._b = b
        self._c = c
        self._d = d
        self._bx = bx
        self._by = by
        self._alpha = alpha
        self._beta = beta
        self._M = M

    def _parametres_positifs(self):
        """Vérification que les arguments sont positifs."""
        for attribut in vars(self):
            if getattr(self, attribut) < 0:
                return False
        return True

    def _regime_bistable(self):
        """Vérification du régime bistable."""
        x_stable = (self._d * self._by - self._c * self._bx < 0)
        y_stable = (self._a * self._bx - self._b * self._by < 0)
        return x_stable and y_stable

    def __call__(self, X, u):
        """Evaluation du flux pour l'état X et le contrôle u.

        :param X: état du système
        :type X: 2-tuple ou numpy.array
        :param u: contrôle
        :type u: float
        """
        assert 0 <= u <= self._M
        x, y = X
        return np.array((x * (self._a * (self._bx - x) - self._b * y
                         - self._alpha * u),
                         y * (self._d * (self._by - y) - self._c * x
                         - self._beta * u)))
