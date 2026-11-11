---
name: setup
description: Install or update the Socratic learning stack in the current repo.
# User-invoked only: setup rewrites the contract file, creates .socratic/ and may install a git hook,
# so the agent must never start it on its own.
disable-model-invocation: true
---

# Socratic setup

Install the Socratic contract and learner state into the current repo, or update them. The rest of the stack (`/socratic:approve`, `/socratic:drill`, the modes) depends on what this writes.

Sources, relative to this skill:
- `../core/CONTRACT.md`: the contract
- `../core/RECORDING.md`: how skills write learner state
- `templates/`: the `.socratic/` files
- `../hooks/pre-commit`: the strict-mode hook

If any is missing, say the `socratic/` folder is incomplete and stop.

## Steps

1. **Detect.** If `.socratic/config.yml` exists, this is an **update**: show the current values and ask only about the ones the human wants to change. Done when you know: fresh install or update.

2. **Interview.** Ask **one question at a time** and recommend an answer each time. Done when all six are settled:
   1. **Mission:** what they want to learn, why, and the target level. This fills `MISSION.md`.
   2. **Roadmap:** propose 8–12 concepts the mission rests on, in prerequisite order, as kebab-case ids with one line each. The human edits the list. This fills `## Roadmap` in `MISSION.md`.
   3. **Install target:** `AGENTS.md` (shared: everyone using an agent here gets the contract; right for a repo they own) or `CLAUDE.local.md` (personal and git-ignored; right for a shared work repo). Recommend `CLAUDE.local.md` if the repo has other contributors. For agents other than Claude Code, use their per-user instructions file instead.
   4. **Learning-critical paths:** propose globs from the repo layout (the core logic, not config or tests plumbing). The human confirms or edits them.
   5. **Gate:** `strict` (the commit is blocked until `/socratic:approve` passes), `nudge` (prompt only), or `off`. Recommend `strict` for a learning repo and `nudge` for real work.
   6. **Hint ceiling:** `L1`–`L4`. Recommend `L4`.

3. **Write state.** Copy `templates/` into `.socratic/`, copy `../core/RECORDING.md` to `.socratic/RECORDING.md`, and fill in the answers. Seed every roadmap concept into `mastery.yml` as `level: unknown, source: mission`. On an update, change only the answered fields: `mastery.yml` and `oversight.yml` keep their history (new roadmap concepts are added as `unknown`), and `RECORDING.md` is refreshed. Done when all five files exist and the YAML parses.

4. **Install the contract** into `contract_file`. Create the file if missing. Replace the block between `<!-- socratic:begin -->` and `<!-- socratic:end -->` with the current `CONTRACT.md`, or append the block if absent. Leave the rest of the file as it is. For `AGENTS.md` only: if `CLAUDE.md` exists and doesn't mention `AGENTS.md`, add one line: `Follow the Socratic contract in AGENTS.md.` Done when the block matches `CONTRACT.md`.

5. **Git.** Unless `commit_state: true`, keep `.socratic/` out of git: in `.gitignore` for a shared install, in `.git/info/exclude` for a personal one (so the shared `.gitignore` is untouched). A personal `CLAUDE.local.md` goes in `.git/info/exclude` too. Done when `git check-ignore .socratic/config.yml` matches the choice.

6. **Hook.** If `gate` is `strict`, install `../hooks/pre-commit` as `.git/hooks/pre-commit` (executable). If a pre-commit hook already exists, keep it and call ours from it. Otherwise leave hooks alone: the hook is a no-op outside strict mode. Done when a strict repo blocks a gated commit that has no `/socratic:approve` pass.

7. **Report.** List the files written, the install target and the gate mode. Then give one next step: `/socratic:tutor` on the first roadmap concept.
