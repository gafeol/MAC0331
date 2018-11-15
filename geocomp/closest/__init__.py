# -*- coding: utf-8 -*-
"""Algoritmos para o problema do Par Mais Proximo:

Dado um conjunto de pontos S, determinar dois cuja distancia entre eles seja minima

Algoritmos disponveis:
- Fora bruta
- Line Sweep
- Divide and conquer
"""
from . import brute
from . import sweep
from . import divide

children = [
	[ 'brute', 'Brute', 'Forca Bruta' ],
	[ 'sweep', 'Sweep', 'Line Sweep'  ],
	[ 'divide', 'Divide', 'Divide and Conquer']
]

__all__ = [a[0] for a in children]
