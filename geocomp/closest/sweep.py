#!/usr/bin/env python


"""Algoritmo de line sweep"""

from geocomp.common.segment import Segment
from geocomp.common.point import Point
from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.config import *
from geocomp.closest.treap import *
from geocomp.closest.square import *
import math
import time


T = Treap()

def Sweep (l):
	"Algoritmo que usa line sweep para encontrar o par de pontos mais proximo"
	if len (l) < 2: return None

	T.clear()

	l.sort(key=lambda o: o.x)
	
	closest = float("inf")
	a = b = None
	id = None
	dt = {}
	ult = 0

	for i in range (len(l)):
		control.freeze_update ()
		hid = l[i].hilight('red')
		vid = control.plot_vert_line(l[i].x)
		oid = None
		if(closest != float("inf")):
			oid = control.plot_vert_line(l[i].x - math.sqrt(closest), COLOR_ALT1)

		# Remocao em O(lgn)
		while(ult < i and math.sqrt(closest) <= l[i].x - l[ult].x):
			T.erasePoint(l[ult])
			l[ult].unhilight(dt[l[ult]])
			ult += 1

		control.thaw_update ()
		control.update ()

		# Checando se atualiza a distancia minima entre pontos em O(lgn)
		## Cria box 
		box_id = lx = None
		rz = 0
		if(closest != float("inf")):
			rz = math.sqrt(closest)
			lx = l[i].x - rz
		box_id = plot_square(lx, l[i].y - rz, l[i].x, l[i].y+rz)
		control.sleep()

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

				rz = math.sqrt(closest)
				if(lx == None):
					lx = l[i].x - rz
				erase_square(box_id)
				box_id = plot_square(lx, l[i].y - rz, l[i].x, l[i].y + rz)

				hia = a.hilight ()
				hib = b.hilight ()
				id = a.lineto (b)

				if(oid == None):
					oid = control.plot_vert_line(l[i].x - math.sqrt(closest), COLOR_ALT1)
				control.sleep()

			o = T.findUpperPoint(o)

		## Remove box
		erase_square(box_id)

		# Insere o ponto na Treap - O(lgn)
		T.insertPoint(l[i])
		l[i].unhilight(hid)
		hi = l[i].hilight(COLOR_ALT1)
		dt[l[i]] = hi

		control.plot_delete (vid)
		if(oid != None):
			control.plot_delete(oid)
		
		control.thaw_update()
		control.update()
	
	
	control.thaw_update()
	control.update()
	for p in l:
		if(p in dt):
			p.unhilight(dt[p])

	a.hilight('green')
	b.hilight('green')
	ret = Segment (a, b)
	ret.extra_info = 'distancia: %.2f'%math.sqrt (dist2 (a, b))
	return ret
