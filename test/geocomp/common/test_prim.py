import math
import unittest

import geocomp.common.prim as prim


class TestPrim(unittest.TestCase):

    def test_angleCCW_withNoneTypeArgument_shouldRaiseValueError(self):
        with self.assertRaises(ValueError):
            prim.ccw_angle(None, [0, 0])

        with self.assertRaises(ValueError):
            prim.ccw_angle([0, 0], None)

    def test_angleCCW_withCollinearVectors_shouldReturnZero(self):
        self.assertEqual(0, prim.ccw_angle([0, 1], [0, 1]))

    def test_angleCCW_withNotCollinearVectors_shouldReturnClockWiseAngleBetweenThem(self):
        self.assertEqual(math.pi / 2, prim.ccw_angle([1, 0], [0, 1]))
        self.assertEqual(math.pi, prim.ccw_angle([1, 0], [-1, 0]))
        self.assertEqual(3 * math.pi / 2, prim.ccw_angle([1, 0], [0, -1]))

    def test_distPtLineSq_withNoneTypeArgument_shouldRaiseValueError(self):
        with self.assertRaises(ValueError):
            prim.dist_pt_line_sq(None, [1, 0], [2, 0])

        with self.assertRaises(ValueError):
            prim.dist_pt_line_sq([1, 0], None, [2, 0])

        with self.assertRaises(ValueError):
            prim.dist_pt_line_sq([1, 0], [2, 0], None)

    def test_distPtLineSq_withPointsFromDifferentDimensions_shouldRaiseValueError(self):
        with self.assertRaises(ValueError):
            prim.dist_pt_line_sq([1, 0], [1, 1, 1], [1, 2])

        with self.assertRaises(ValueError):
            prim.dist_pt_line_sq([1, 0, 1], [1, 1], [1, 2])

        with self.assertRaises(ValueError):
            prim.dist_pt_line_sq([1, 0], [1, 1], [1, 2, 2])

    def test_distPtLineSq_withPointOnSegment_shouldReturnZero(self):
        self.assertEqual(0, prim.dist_pt_line_sq([2, 0], [1, 0], [3, 0]))

        self.assertEqual(0, prim.dist_pt_line_sq([0, 2], [0, 1], [0, 3]))

        self.assertEqual(0, prim.dist_pt_line_sq([-2, 0], [-1, 0], [-3, 0]))

        self.assertEqual(0, prim.dist_pt_line_sq([0, -2], [0, -1], [0, -3]))

        self.assertEqual(0, prim.dist_pt_line_sq([1, 1], [0, 0], [2, 2]))

        self.assertEqual(0, prim.dist_pt_line_sq([-1, 1], [0, 0], [-2, 2]))

        self.assertEqual(0, prim.dist_pt_line_sq([-1, -1], [0, 0], [-2, -2]))

        self.assertEqual(0, prim.dist_pt_line_sq([1, -1], [0, 0], [2, -2]))

        self.assertEqual(0, prim.dist_pt_line_sq([2, 0], [1, 0], [3, 0]))

    def test_distPtLineSq_withPointNotOnSegment_shouldReturnSquaredDistanceFromPointToLine(self):
        self.assertEqual(14 / 4, prim.dist_pt_line_sq([1, 1, -1], [0, -1, -1], [1, 0, 1]))
        self.assertEqual(14 / 4, prim.dist_pt_line_sq([1, 1, -1], [1, 0, 1], [0, -1, -1],))
