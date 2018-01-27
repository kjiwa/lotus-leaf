"""Defines the test suite for server unit tests."""

import unittest
import gendata_db_test
import gendata_test


def testsuite():
  """Creates a new test suite for server tests."""
  loader = unittest.TestLoader()
  ts = unittest.TestSuite()
  ts.addTests(loader.loadTestsFromTestCase(gendata_db_test.GendataDbTestCase))
  ts.addTests(loader.loadTestsFromTestCase(gendata_test.GendataTestCase))
  return ts


if __name__ == '__main__':
  unittest.TextTestRunner(verbosity=2).run(testsuite())
