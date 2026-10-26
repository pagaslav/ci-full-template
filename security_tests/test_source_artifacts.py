"""Ensure a source checkout never carries a versioned runtime SQLite database."""
from pathlib import Path
import re
import subprocess
import unittest

class SourceArtifactTests(unittest.TestCase):
    def test_no_runtime_database_or_sidecar_is_versioned(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(['git', 'ls-files', '-z'], cwd=root, check=True, capture_output=True, text=True)
        paths = result.stdout.split('\0')
        databases = [path for path in paths if re.search(r'\.(?:sqlite3?|db)(?:$|-)', path, re.IGNORECASE)]
        self.assertEqual(databases, [], 'Runtime data belongs outside the versioned source checkout.')
