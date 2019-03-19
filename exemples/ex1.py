#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 perrollaz <perrollaz@vincent-MacBookPro>
#
# Distributed under terms of the MIT license.

"""
Exemple d'utilisation du module.
"""

from hjb.cartographie import Valeur
from hjb.systeme import Systeme
import hjb.affichage as aff

s = Systeme(a=1, b=2, c=2, d=1, M=1, alpha=0.75, beta=5. / 8, bx=1, by=1)
v = Valeur.from_dl(sys=s, T=10, dl=0.02)
v.resolution()
fc = aff.affichage_contour(v)
fc.show()
