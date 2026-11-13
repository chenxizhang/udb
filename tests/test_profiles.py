import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "bin/udb").read_text()
OPTIONS = "login_requested=1" + SOURCE.split("login_requested=1", 1)[1].split(
    'show_progress "Checking platform and native prerequisites"', 1
)[0]
AZURE = "azure_login_arguments=()" + SOURCE.split(
    "azure_login_arguments=()", 1
)[1].split("\nlogin_command_status=0", 1)[0]
INSTALL = "if (( workiq_requested == 1 )); then" + SOURCE.split(
    "if (( workiq_requested == 1 )); then", 1
)[1].split("\nrun_step copilot ", 1)[0]
LOGIN = SOURCE.split(
    "if (( login_requested == 1 )) && ( : </dev/tty ) 2>/dev/null; then", 1
)[1].split("\nprint_setup_summary | tee", 1)[0]


class ProfileTests(unittest.TestCase):
    def run_profile(self, args, terminal=True):
        helpers = """
run_step() { printf 'RUN %s\\n' "$1"; }
skip_step() { printf 'SKIP %s: %s\\n' "$1" "$3"; }
printf 'TENANT=%s\\n' "$azure_tenant"
printf 'LOGIN_COUNT=%s\\n' "${#azure_login_arguments[@]}"
printf 'TOKEN_COUNT=%s\\n' "${#azure_token_arguments[@]}"
if (( ${#azure_login_arguments[@]} > 0 )); then
    printf 'LOGIN_ARG=%s\\n' "${azure_login_arguments[@]}"
    printf 'TOKEN_ARG=%s\\n' "${azure_token_arguments[@]}"
fi
"""
        script = (
            "set -Eeuo pipefail\n" + OPTIONS + "\n" + AZURE + helpers + INSTALL
            + f"\nif (( login_requested == 1 && {int(terminal)} == 1 )); then"
            + LOGIN
        )
        return subprocess.run(
            ["/bin/bash", "-c", script, "test-profile", *args],
            capture_output=True, text=True, timeout=5,
        )

    def test_no_profile_injects_an_azure_tenant(self):
        for args in ([], ["-w"], ["-wc"], ["-p"], ["-pc"], ["-c"]):
            with self.subTest(args=args):
                result = self.run_profile(args, terminal=False)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("TENANT=\nLOGIN_COUNT=0\nTOKEN_COUNT=0\n", result.stdout)
                self.assertIn("Manual login: az login\n", result.stdout)
                self.assertNotIn("--tenant", result.stdout)

    def test_explicit_tenant_is_used_for_login_and_token_checks(self):
        for args in (
            ["-t", "tenant.example"],
            ["-p", "--tenant", "tenant.example"],
            ["-wc", "-t", "tenant.example"],
        ):
            with self.subTest(args=args):
                result = self.run_profile(args, terminal=False)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(
                    "LOGIN_ARG=--tenant\nLOGIN_ARG=tenant.example\n"
                    "LOGIN_ARG=--skip-subscription-discovery\n"
                    "TOKEN_ARG=--tenant\nTOKEN_ARG=tenant.example\n",
                    result.stdout,
                )
                self.assertIn(
                    "Manual login: az login --tenant tenant.example "
                    "--skip-subscription-discovery\n", result.stdout,
                )

    def test_default_and_work_profiles_still_skip_workiq_without_tenant(self):
        for args in ([], ["-c"], ["-w"], ["--work"], ["-wc"], ["--skip-login"]):
            for terminal in (True, False):
                with self.subTest(args=args, terminal=terminal):
                    result = self.run_profile(args, terminal)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    for step in ("workiq", "workiq-runtime", "login-workiq"):
                        self.assertIn(f"SKIP {step}:", result.stdout)
                        self.assertNotIn(f"RUN {step}\n", result.stdout)
                    self.assertNotIn("Manual login: workiq", result.stdout)

    def test_personal_or_explicit_tenant_keeps_workiq(self):
        for args in (["-p"], ["-pc"], ["-w", "-t", "tenant.example"]):
            with self.subTest(args=args):
                result = self.run_profile(args)
                self.assertEqual(result.returncode, 0, result.stderr)
                for step in ("workiq", "workiq-runtime", "login-workiq"):
                    self.assertIn(f"RUN {step}\n", result.stdout)
                headless = self.run_profile(args, terminal=False)
                self.assertEqual(headless.returncode, 0, headless.stderr)
                self.assertIn("Manual login: workiq auth login", headless.stdout)
                self.assertIn("SKIP login-workiq:", headless.stdout)

    def test_invalid_options_fail_before_initialization(self):
        for args in (["-w", "-p"], ["-t"], ["--tenant", ""], ["-t", "--skip-login"]):
            with self.subTest(args=args):
                result = self.run_profile(args)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("RUN ", result.stdout)

    def test_direct_and_streamed_help_do_not_initialize_the_home(self):
        with tempfile.TemporaryDirectory() as directory:
            env = dict(os.environ, HOME=directory, PATH="/usr/bin:/bin")
            for streamed in (False, True):
                with self.subTest(streamed=streamed):
                    command = (
                        ["/bin/bash", "-s", "--", "--help"] if streamed
                        else [str(ROOT / "bin/udb"), "--help"]
                    )
                    result = subprocess.run(
                        command, input=SOURCE if streamed else None, env=env,
                        capture_output=True, text=True, timeout=10,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("udb -- Ubuntu Development Bootstrap", result.stdout)
                    self.assertIn("both profiles use plain az login", result.stdout)
                    self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
