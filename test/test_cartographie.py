#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from hjb.cartographie import Valeur
from hjb.systeme import Systeme


def test_instanciation():
    s = Systeme(a=1, b=1, c=1, d=1, bx=1, by=1, alpha=1, beta=1, M=1)
    v = Valeur(sys=s, T=10, dl=0.1)
    assert isinstance(v, Valeur)
