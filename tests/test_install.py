import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def test_staged_install_provides_a_command_without_initializing_the_home(self):
        for prefix in ("/usr", "/opt/udb tools"):
            with self.subTest(prefix=prefix), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                home = root / "home"
                home.mkdir()
                staging = root / "staging"
                env = dict(os.environ, HOME=str(home), PATH="/usr/bin:/bin")
                result = subprocess.run(
                    ["make", "--no-print-directory", "install", f"PREFIX={prefix}",
                     f"DESTDIR={staging}"],
                    cwd=ROOT, env=env, capture_output=True, text=True, timeout=10,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                installed = staging / prefix.lstrip("/") / "bin/udb"
                help_result = subprocess.run(
                    [str(installed), "--help"], cwd=home, env=env,
                    capture_output=True, text=True, timeout=10,
                )
                self.assertEqual(help_result.returncode, 0, help_result.stderr)
                self.assertIn("udb -- Ubuntu Development Bootstrap", help_result.stdout)
                self.assertEqual(list(home.iterdir()), [])
                documents = staging / prefix.lstrip("/") / "share/doc/udb"
                self.assertTrue((documents / "LICENSE").is_file())
                self.assertTrue((documents / "README.md").is_file())


if __name__ == "__main__":
    unittest.main()
