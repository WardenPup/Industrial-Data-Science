"""Focused integrity, boundary and source-result checks for Exercise 14.1."""
import unittest

import pandas as pd

from sessions.ch14.tool_wear import WEAR, load_data, wear_tables


class ToolWearTests(unittest.TestCase):
    def test_interval_boundaries_and_nonmutation(self):
        data = pd.DataFrame({"UDI": [1, 2, 3, 4, 5], WEAR: [198, 200, 240, 241, 253],
                             "TWF": [1, 1, 0, 1, 1], "Machine failure": [1, 1, 0, 1, 1]})
        original = data.copy(deep=True)
        bands, threshold, outside = wear_tables(data)
        self.assertEqual(bands["Datensätze"].tolist(), [1, 2, 2])
        self.assertEqual(bands["TWF=1"].tolist(), [1, 1, 2])
        self.assertEqual(threshold["TWF=1"].tolist(), [2, 2])
        self.assertEqual(outside.UDI.tolist(), [1, 4, 5])
        pd.testing.assert_frame_equal(data, original)

    def test_invalid_wear_and_flags(self):
        for wear, flag in [(-1, 1), (float("nan"), 1), (200, 2), ("200", 1)]:
            with self.subTest(wear=wear, flag=flag), self.assertRaises(ValueError):
                wear_tables(pd.DataFrame({WEAR: [wear], "TWF": [flag]}))

    def test_pinned_source_and_independent_counts(self):
        data = load_data()  # SHA256 and full source quality checks are mandatory.
        bands, threshold, outside = wear_tables(data)
        self.assertEqual(int(data.TWF.sum()), 46)
        self.assertEqual(bands["Datensätze"].tolist(), [9199, 790, 11])
        self.assertEqual(bands["TWF=1"].tolist(), [1, 43, 2])
        self.assertEqual(threshold["Datensätze"].tolist(), [9328, 672])
        self.assertEqual(threshold["TWF=1"].tolist(), [2, 44])
        self.assertEqual(outside.UDI.tolist(), [1997, 2865, 5402])
        self.assertEqual(outside[WEAR].tolist(), [198, 246, 253])
        self.assertTrue(data.loc[data.TWF.eq(1), "Machine failure"].eq(1).all())


if __name__ == "__main__":
    unittest.main()
