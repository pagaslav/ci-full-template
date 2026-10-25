import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch


class SettingsLoggingTests(unittest.TestCase):
    def test_startup_does_not_disclose_synthetic_credentials(self):
        # These sentinels are deliberately fake and never used for a connection.
        for development in ('True', 'False'):
            output = io.StringIO()
            values = {'DEVELOPMENT': development, 'SECRET_KEY': 'sentinel-secret-never-log', 'DATABASE_URL': 'postgres://sentinel-user:sentinel-password@example.invalid/fake'}
            with patch.dict(os.environ, values, clear=True), contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                result = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'django_todo/settings.py'))
            self.assertEqual(result['SECRET_KEY'], values['SECRET_KEY'])
            for sensitive in ('sentinel-secret-never-log', 'sentinel-password', values['DATABASE_URL']):
                self.assertNotIn(sensitive, output.getvalue())
