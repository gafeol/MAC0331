#!/usr/bin/env python
"""Algoritmo de line sweep"""

# BUG: 0

from geocomp.common.segment import Segment
from geocomp.common.point import Point
from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.config import *
import math
import time

def sq(x):
	return x*x

oo = float("inf")


ans = oo
a = None
hia = None
b = None
hib = None
id = None

def closest_pair(v, w, l, r):
	global ans, a, b, id, hia, hib

	if l + 1 >= r: 
		return oo
	
	m = int((l + r)/2)
	x = v[m].x
	
	#Vertical line dividing
	vid = control.plot_vert_line(v[m].x)
	control.sleep()

	res = min(closest_pair(v, w, l, m), closest_pair(v, w, m, r))

	control.plot_delete(vid)

	# Merge
	i = l
	j = m
	aux = l

	pa = pb = None
	while i < m and j < r :
		if v[i].y < v[j].y:
			w[aux] = v[i]
			i = i+1
		else:
			w[aux] = v[j]
			j = j+1
		aux = aux+1

	while i < m:
		w[aux] = v[i]
		aux = aux+1
		i = i + 1

	while j < r:
		w[aux] = v[j]
		aux = aux+1
		j = j+1

	s = l
	for i in range(l, r):
		v[i] = w[i]
		if sq(v[i].x - x) < sq(res):
			for j in range(s-1, l-1, -1):
				if sq(w[i].y - w[j].y) >= res*res:
					break;
				dis = math.sqrt(dist2(w[i], w[j]))

				res = min(res, dis)

				if ans > res:
					ans = res
					control.freeze_update()
					if a != None: a.unhilight(hia)
					if b != None: b.unhilight(hib)
					if(id != None): control.plot_delete(id)

					a = w[i]
					b = w[j]

					hia = a.hilight()
					hib = b.hilight()
					id = a.lineto(b)

					control.thaw_update()
					control.update()

			w[s] = v[i]
			s = s+1
	return res
					

def Divide (l):
	"Algoritmo que usa divide and conquer para encontrar o par de pontos mais proximo"
	global ans, a, b

	if len (l) < 2: 
		return None
	ans = oo
	a = None
	b = None

	# Ordena por x os pontos recebidos
	l.sort(key=lambda o: o.x)
	
# Como que aloca len(l) posicoes na nova lista
	L = []
	for i in range(len(l)):
		L.append(0)

	dis = closest_pair(l, L, 0, len(l))

	# PRINTAR INFOS NO FINAL
	ret = Segment (a, b)
	ret.extra_info = 'distancia: %.2f'%dis
	return ret
	
