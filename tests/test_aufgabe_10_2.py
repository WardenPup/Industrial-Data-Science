"""Verify source selection and defensive handling, without modelling the data."""

import unittest

from sessions.ch10.ai4i_data import COLUMNS, load_ai4i, validate_data


class AI4IDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_ai4i()

    def test_official_shape_and_first_observation(self):
        self.assertEqual(self.data.shape, (10000, 4))
        self.assertEqual(list(self.data.columns), COLUMNS)
        self.assertEqual(self.data.iloc[0].tolist(), [1, 42.8, 1551, 298.1])

    def test_missing_value_rejected(self):
        altered = self.data.copy()
        altered.loc[0, "Torque [Nm]"] = float("nan")
        with self.assertRaises(ValueError):
            validate_data(altered)

    def test_duplicate_identifier_rejected(self):
        altered = self.data.copy()
        altered.loc[1, "UDI"] = 1
        with self.assertRaises(ValueError):
            validate_data(altered)

    def test_wrong_columns_rejected(self):
        with self.assertRaises(ValueError):
            validate_data(self.data.drop(columns="Torque [Nm]"))


if __name__ == "__main__":
    unittest.main()
