import unittest
import math

import numpy as np

from em_clustering import dvmnorm


class TestDmvnorm(unittest.TestCase):
    def test_trivial_1(self):
        result = dvmnorm(np.array([0, 0]), np.array([0, 0]), np.eye(2))
        self.assertAlmostEqual(0.5 / math.pi, result)

    def test_trivial_2(self):
        result = dvmnorm(np.array([0, 0]), np.array([1, 1]), np.eye(2))
        self.assertAlmostEqual(0.5 / math.pi / math.exp(1), result)
