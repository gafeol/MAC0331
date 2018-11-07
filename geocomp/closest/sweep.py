#!/usr/bin/env python
"""Algoritmo de line sweep"""

from geocomp.common.segment import Segment
from geocomp.common.point import Point
from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.config import *
import math


List = []

def comparax(x, y):
	return x.x - y.x

def Sweep (l):
	"Algoritmo que usa line sweep para encontrar o par de pontos mais proximo"

	if len (l) < 2: return None

	List.clear()

# Ordena por x os pontos recebidos
	l.sort(key=lambda o: o.x)
	
	oo = 10000
	closest = float("inf")
	a = b = None
	id = None

	dt = {}

	for i in range (len(l)):
		inf_down = Point(l[i].x, -oo)
		inf_up   = Point(l[i].x, oo)
		# Melhorar impressao de linha, tornar cor branca
		line_plot = inf_down.lineto(inf_up)
		control.thaw_update ()
		control.update ()

		for j in List:
			# Checa o segmento de y em O(n) 
            #TODO: achar segmento em log(n)

			if(abs(l[j].y - l[i].y) < math.sqrt(closest)):
				dist = dist2 (l[i], l[j])
				if dist < closest:
					control.freeze_update ()
					if a != None: a.unhilight (hia)
					if b != None: b.unhilight (hib)
					if id != None: control.plot_delete (id)

					closest = dist
					a = l[i]
					b = l[j]

					hia = a.hilight ()
					hib = b.hilight ()
					id = a.lineto (b)
					control.thaw_update ()
					control.update ()

		# Remocao do line sweep em O(n)
        # TODO: Realizar remocao em O(lgn)
		for j in List:
			if math.sqrt(closest) < l[i].x - l[j].x:
				List.remove(j)
				l[j].unhilight(dt[l[j]])

		List.append(i)
		hi = l[i].hilight(COLOR_ALT1)
		dt[l[i]] = hi

		control.plot_delete (line_plot)
		
		control.thaw_update()
		control.update()
	
	for j in List:
		l[j].unhilight(dt[l[j]])

	control.thaw_update()
	control.update()

	ret = Segment (a, b)
	ret.extra_info = 'distancia: %.2f'%math.sqrt (dist2 (a, b))
	return ret
