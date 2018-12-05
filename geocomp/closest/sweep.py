#!/usr/bin/env python
"""Algoritmo de line sweep"""

from geocomp.common.segment import Segment
from geocomp.common.point import Point
from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.config import *
from geocomp.closest.treap import *
import math
import time


T = Treap()

vert_lines = []

def hachura(l, r):
	global vert_lines
	for ln in vert_lines:
		control.plot_delete(ln)

	if(l == float("inf")):
		return 
	stp = (r - l)/10.

	while(l+stp < r):
		vid = control.plot_vert_line(l+stp, COLOR_ALT2)
		vert_lines.append(vid)
		l += stp
	
def clear():
	global vert_lines
	for ln in vert_lines:
		control.plot_delete(ln)
	

def Sweep (l):
	"Algoritmo que usa line sweep para encontrar o par de pontos mais proximo"
	if len (l) < 2: return None

	#List.clear()
	T.clear()

	# Ordena por x os pontos recebidos
	l.sort(key=lambda o: o.x)
	
	closest = float("inf")
	a = b = None
	id = None
	dt = {}
	ult = 0

	for i in range (len(l)):
		# Melhorar impressao de linha, tornar cor branca

		vid = control.plot_vert_line(l[i].x)
		oid = None
		if(closest != float("inf")):
			oid = control.plot_vert_line(l[i].x - math.sqrt(closest))
			hachura(l[i].x - math.sqrt(closest), l[i].x)
		control.sleep()
		control.thaw_update ()
		control.update ()

		# Remocao em O(lgn)
		while(ult < i and math.sqrt(closest) < l[i].x - l[ult].x):
			T.erasePoint(l[ult])
			l[ult].unhilight(dt[l[ult]])
			ult += 1


		mn = Point(l[i].x, l[i].y - math.sqrt(closest))
		o = T.findPoint(mn);
		while(o != None and abs(o.y-l[i].y) <= math.sqrt(closest)):
			dist = dist2 (l[i], o)
			if dist < closest:
				control.freeze_update ()
				if a != None: a.unhilight (hia)
				if b != None: b.unhilight (hib)
				if id != None: control.plot_delete (id)

				closest = dist
				a = l[i]
				b = o

				hia = a.hilight ()
				hib = b.hilight ()
				id = a.lineto (b)

				if(oid != None):
					control.plot_delete(oid)
				oid = control.plot_vert_line(l[i].x - math.sqrt(closest))
				hachura(l[i].x - math.sqrt(closest), l[i].x)
				control.thaw_update ()
				control.update ()

			o = T.findUpperPoint(o)

		#List.append(i)
		T.insertPoint(l[i])
		hi = l[i].hilight(COLOR_ALT1)
		dt[l[i]] = hi

		control.plot_delete (vid)
		if(oid != None):
			control.plot_delete(oid)
		
		control.thaw_update()
		control.update()
	
	for p in l:
		p.unhilight(dt[p])
	
	clear()

	control.thaw_update()
	control.update()

	ret = Segment (a, b)
	ret.extra_info = 'distancia: %.2f'%math.sqrt (dist2 (a, b))
	return ret
