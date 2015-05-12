# Copyright (c) 2015, Matt Layman

import tempfile
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from tap import TAPTestRunner
from tap.runner import TAPTestResult, _tracker


class TestTAPTestRunner(unittest.TestCase):

    def test_has_tap_test_result(self):
        runner = TAPTestRunner()
        self.assertEqual(runner.resultclass, TAPTestResult)

    def test_runner_uses_outdir(self):
        """Test that the test runner sets the outdir so that TAP
        files will be written to that location.

        Setting class attributes to get the right behavior is a dirty hack, but
        the unittest classes aren't very extensible.
        """
        # Save the previous outdir in case **this** execution was using it.
        previous_outdir = _tracker.outdir
        outdir = tempfile.mkdtemp()

        TAPTestRunner.set_outdir(outdir)

        self.assertEqual(outdir, _tracker.outdir)

        _tracker.outdir = previous_outdir

    def test_runner_uses_format(self):
        """Test that format is set on TAPTestResult FORMAT."""
        # Save the previous format in case **this** execution was using it.
        previous_format = TAPTestResult.FORMAT
        fmt = "{method_name}: {short_description}"

        TAPTestRunner.set_format(fmt)

        self.assertEqual(fmt, TAPTestResult.FORMAT)

        TAPTestResult.FORMAT = previous_format

    @mock.patch('sys.exit')
    def test_bad_format_string(self, fake_exit):
        """A bad format string exits the runner."""
        previous_format = TAPTestResult.FORMAT
        bad_format = "Not gonna work {sort_desc}"
        TAPTestRunner.set_format(bad_format)
        result = TAPTestResult(None, True, 1)
        test = mock.Mock()

        result._description(test)

        self.assertTrue(fake_exit.called)

        TAPTestResult.FORMAT = previous_format
