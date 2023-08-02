import unittest

from tape_computer.utils import *
from tape_computer.errors import DataTypeError


class TestUtils(unittest.TestCase):
    def test_is_numeric_when_non_numeric_returns_false(self):
        value = "123hello"
        self.assertFalse(is_numeric(value))

    def test_is_numeric_when_numeric_returns_true(self):
        value = "12345"
        self.assertTrue(is_numeric(value))

    def test_range_check_unsigned_out_of_range_higher_end(self):
        with self.assertRaises(DataTypeError):
            range_check(2500, 0, 8, "u8")

    def test_range_check_unsigned_out_of_range_lower_end(self):
        with self.assertRaises(DataTypeError):
            range_check(-20, 0, 8, "u8")

    def test_range_check_unsigned_in_range(self):
        self.assertIsNone(range_check(250, 0, 8, "u8"))

    def test_range_check_signed_out_of_range_higher_end(self):
        with self.assertRaises(DataTypeError):
            range_check(200, 8, 8, "i8")

    def test_range_check_signed_out_of_range_lower_end(self):
        with self.assertRaises(DataTypeError):
            range_check(-200, 8, 8, "i8")

    def test_range_check_signed_in_range(self):
        self.assertIsNone(range_check(120, 8, 8, "i8"))
        self.assertIsNone(range_check(-120, 8, 8, "i8"))

    def test_get_int_from_str_passed_val_is_not_numeric(self):
        with self.assertRaises(DataTypeError):
            get_int_from_str("123hello", "i8")

    def test_get_int_from_str_success(self):
        self.assertEqual(get_int_from_str("1234", "i32"), 1234)