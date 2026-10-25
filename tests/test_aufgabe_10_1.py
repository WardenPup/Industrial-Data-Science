"""Independent mathematical checks and a real image export."""

import tempfile
import unittest
from pathlib import Path

from sessions.ch10.aufgabe_10_1 import heart_coordinates, save_plot
import matplotlib.image as mpimg
import numpy as np


class HeartCurveTests(unittest.TestCase):
    def test_known_quarter_period_points(self):
        x, y = heart_coordinates(5)
        np.testing.assert_allclose(x, [0, 16, 0, -16, 0], atol=1e-12)
        np.testing.assert_allclose(y, [5, 4, -17, 4, 5], atol=1e-12)

    def test_period_closure_symmetry_and_finite_values(self):
        x, y = heart_coordinates()
        self.assertEqual(x.shape, (1001,))
        self.assertTrue(np.isfinite(x).all() and np.isfinite(y).all())
        np.testing.assert_allclose([x[0], y[0]], [x[-1], y[-1]], atol=1e-12)
        np.testing.assert_allclose(x, -x[::-1], atol=1e-12)
        np.testing.assert_allclose(y, y[::-1], atol=1e-12)

    def test_invalid_sample_counts(self):
        for value in (0, 1, 2, -3, 3.5, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                heart_coordinates(value)

    def test_png_export(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "nested/heart.png"
            self.assertEqual(save_plot(output), output)
            pixels = mpimg.imread(output)
            self.assertEqual(pixels.shape[:2], (1120, 1120))
            self.assertGreater(float(pixels.std()), 0.05)


if __name__ == "__main__":
    unittest.main()
