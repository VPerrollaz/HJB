#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 perrollaz <perrollaz@vincent-MacBookPro>
#
# Distributed under terms of the MIT license.

"""
Tests de flux.
"""

from flux import Flux


def test_instanciation():
    f = Flux(a=1, b=1, c=1, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    assert isinstance(f, Flux)


def test_parametres_valides():
    f1 = Flux(a=1, b=1, c=1, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    assert f1._parametres_positifs()

    f2 = Flux(a=-1, b=1, c=1, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    assert not f2._parametres_positifs()


def test_bistabilitite():
    f1 = Flux(a=1, b=1, c=1, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    assert not f1._regime_bistable()

    f2 = Flux(a=1, b=2, c=2, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    assert f2._regime_bistable()
