import unittest

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.cli import parse_args
from src.validation import ValidationError, validate_max_depth


class ConfigTests(unittest.TestCase):

    def test_minimal_args(self):
        cfg = parse_args([
            "--package", "org.example:lib",
            "--source", "https://repo.maven.apache.org",
        ])
        self.assertEqual(cfg.package, "org.example:lib")
        self.assertEqual(cfg.max_depth, 5)
        self.assertFalse(cfg.test_mode)

    def test_full_args(self):
        cfg = parse_args([
            "--package", "p",
            "--source", "file.txt",
            "--test-mode",
            "--ascii-tree",
            "--max-depth", "10",
            "--filter", "spring",
        ])
        self.assertTrue(cfg.test_mode)
        self.assertTrue(cfg.ascii_tree)
        self.assertEqual(cfg.max_depth, 10)
        self.assertEqual(cfg.filter_substring, "spring")


class ValidationTests(unittest.TestCase):
    def test_depth_too_small(self):
        with self.assertRaises(ValidationError):
            validate_max_depth(0)

    def test_depth_too_large(self):
        with self.assertRaises(ValidationError):
            validate_max_depth(101)


if __name__ == "__main__":
    unittest.main()