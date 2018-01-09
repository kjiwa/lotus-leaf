"""Defines the test suite for server unit tests."""

import unittest
import api_server_test
import codec_test


def testsuite():
  """Creates a new test suite for server tests."""
  loader = unittest.TestLoader()
  ts = unittest.TestSuite()
  ts.addTests(loader.loadTestsFromTestCase(api_server_test.ApiServerTestCase))
  ts.addTests(loader.loadTestsFromTestCase(codec_test.CodecTestCase))
  return ts


if __name__ == '__main__':
  unittest.TextTestRunner(verbosity=2).run(testsuite())
