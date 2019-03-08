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
