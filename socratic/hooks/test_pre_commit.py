"""Runs the Socratic pre-commit hook against throwaway git repos."""
import os, shutil, subprocess, tempfile, unittest

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pre-commit")


class PreCommit(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp()
        self.git("init", "-q")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "t")
        shutil.copy(HOOK, os.path.join(self.repo, ".git", "hooks", "pre-commit"))
        os.makedirs(os.path.join(self.repo, ".socratic", "approvals"))

    def tearDown(self):
        shutil.rmtree(self.repo)

    def git(self, *args, env=None):
        return subprocess.run(["git", *args], cwd=self.repo, capture_output=True, text=True,
                              env=dict(os.environ, **(env or {})))

    def gate(self, mode, extra="gate_min_lines: 0\n"):
        with open(os.path.join(self.repo, ".socratic", "config.yml"), "w") as f:
            f.write(f"gate: {mode}   # comment\nhint_ceiling: L4\n{extra}")

    def stage(self, text, path="a.txt"):
        full = os.path.join(self.repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(text)
        self.git("add", path)

    def staged_hash(self):
        return self.git("write-tree").stdout.strip()

    def approve(self):
        open(os.path.join(self.repo, ".socratic", "approvals", self.staged_hash()), "w").close()

    def commit(self, env=None):
        return self.git("commit", "-q", "-m", "x", env=env)

    def test_no_config_allows(self):
        os.rmdir(os.path.join(self.repo, ".socratic", "approvals"))
        os.rmdir(os.path.join(self.repo, ".socratic"))
        self.stage("1")
        self.assertEqual(self.commit().returncode, 0)

    def test_nudge_and_off_allow(self):
        for mode in ("nudge", "off"):
            self.gate(mode)
            self.stage(mode)
            self.assertEqual(self.commit().returncode, 0, mode)

    def test_strict_blocks_without_pass(self):
        self.gate("strict")
        self.stage("1")
        r = self.commit()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("commit blocked", r.stderr)

    def test_strict_allows_with_pass(self):
        self.gate("strict")
        self.stage("1")
        self.approve()
        self.assertEqual(self.commit().returncode, 0)

    def test_stale_pass_blocks(self):
        self.gate("strict")
        self.stage("1")
        self.approve()
        self.stage("2")  # diff changed after approval
        self.assertNotEqual(self.commit().returncode, 0)

    def test_escape_allows_and_logs(self):
        self.gate("strict")
        self.stage("1")
        h = self.staged_hash()
        r = self.commit(env={"SOCRATIC_ESCAPE": "1", "SOCRATIC_REASON": "prod outage"})
        self.assertEqual(r.returncode, 0, r.stderr)
        log = open(os.path.join(self.repo, ".socratic", "escapes.log")).read()
        self.assertIn(h, log)
        self.assertIn("prod outage", log)

    def test_id_ignores_diff_config(self):
        # the agent's and the human's git config can differ; the id must not
        self.gate("strict")
        self.stage("1")
        self.approve()
        self.git("config", "diff.noprefix", "true")
        self.assertEqual(self.commit().returncode, 0)

    def test_gate_paths_scope(self):
        self.gate("strict", "gate_paths:\n  - src/**   # code only\ngate_min_lines: 0\n")
        self.stage("docs", "docs/readme.md")
        self.assertEqual(self.commit().returncode, 0)  # outside gate_paths
        self.stage("code", "src/deep/x.py")
        self.assertNotEqual(self.commit().returncode, 0)  # inside gate_paths

    def test_min_lines_lets_small_commits_through(self):
        self.gate("strict", "gate_min_lines: 3\n")
        self.stage("one line\n")
        self.assertEqual(self.commit().returncode, 0)
        self.stage("a\nb\nc\nd\n")
        self.assertNotEqual(self.commit().returncode, 0)


if __name__ == "__main__":
    unittest.main()
