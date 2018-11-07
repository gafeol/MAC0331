# -*- coding: utf-8 -*-
"""Algoritmos para o problema do Par Mais Proximo:

Dado um conjunto de pontos S, determinar dois cuja distancia entre eles seja minima

Algoritmos disponveis:
- Fora bruta
- Line Sweep
"""
from . import brute
from . import sweep

children = [
	[ 'brute', 'Brute', 'Forca Bruta' ],
	[ 'sweep', 'Sweep', 'Line Sweep'  ]
]

__all__ = [a[0] for a in children]
