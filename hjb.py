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
            \dot{x} = x (a (\\bar{x} - x) - b y) - \\alpha x u\\
            \dot{y} = y (d (\\bar{y} - y) - c x) - \\beta y u
        \end{cases}
    \end{equation}
"""
