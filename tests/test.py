#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os

testdir = os.path.dirname(__file__)
srcdir = "../clarity"
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))


import unittest
import clarity as log

from colored import fore, style
from typing import Dict
from unittest.mock import patch


class TestClarity(unittest.TestCase):
    """Unit tests for clarity logger."""

    def _run_test(self, method: str, color: str, use_str: bool = True) -> None:
        with patch("clarity.logging.{}".format(method)) as mocked_method:
            message = "test {} message".format(method)
            if use_str:
                expected = color + message + style.RESET
                getattr(log, method)(message)
            else:
                expected = color + "{{'msg': '{}'}}".format(message) + style.RESET
                getattr(log, method)({"msg": message})
            mocked_method.assert_called_with(expected)

    def test_all_methods(self) -> None:
        cases: Dict[str, str] = {
            "exception": fore.ORANGE_1,
            "fatal": fore.RED,
            "error": fore.LIGHT_RED,
            "warning": fore.YELLOW,
            "info": fore.DARK_GRAY,
            "debug": fore.STEEL_BLUE,
        }
        for level, color in cases.items():
            self._run_test(level, color)

    def test_non_str_messages(self) -> None:
        cases: Dict[str, str] = {
            "exception": fore.ORANGE_1,
            "fatal": fore.RED,
            "error": fore.LIGHT_RED,
            "warning": fore.YELLOW,
            "info": fore.DARK_GRAY,
            "debug": fore.STEEL_BLUE,
        }
        for level, color in cases.items():
            self._run_test(level, color, use_str=False)


def suite():
    """Test suite"""
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestClarity))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
