---
name: socratic-setup
description: Install or update the Socratic learning stack in the current repo.
disable-model-invocation: true
---

# Socratic setup

Install the Socratic contract and learner state into the current repo, or update them. The rest of the stack (`/approve`, `/drill`, the modes) depends on what this writes.

Sources, relative to this skill:
- `../core/CONTRACT.md`: the contract
- `templates/`: the `.socratic/` files
- `../hooks/pre-commit`: the strict-mode hook

If either is missing, say the `socratic/` folder is incomplete and stop.

## Steps

1. **Detect.** If `.socratic/config.yml` exists, this is an **update**: show the current values and ask only about the ones the human wants to change. Done when you know: fresh install or update.

2. **Interview.** Ask **one question at a time** and recommend an answer each time. Done when all four are settled:
   1. **Mission:** what they want to learn, why, and the target level. This fills `MISSION.md`.
   2. **Learning-critical paths:** propose globs from the repo layout (the core logic, not config or tests plumbing). The human confirms or edits them.
   3. **Gate:** `strict` (the commit is blocked until `/approve` passes), `nudge` (prompt only), or `off`. Recommend `strict` for a learning repo and `nudge` for real work.
   4. **Hint ceiling:** `L1`–`L4`. Recommend `L4`.

3. **Write state.** Copy `templates/` into `.socratic/` and fill in the answers. On an update, change only the answered fields: `mastery.yml` and `oversight.yml` keep their history. Done when all four files exist and parse.

4. **Install the contract.** In `AGENTS.md` (create it if missing), replace the block between `<!-- socratic:begin -->` and `<!-- socratic:end -->` with the current `CONTRACT.md`, or append the block if absent. Leave the rest of the file as it is. If `CLAUDE.md` exists and doesn't mention `AGENTS.md`, add one line: `Follow the Socratic contract in AGENTS.md.` Done when the block in `AGENTS.md` matches `CONTRACT.md`.

5. **Git.** Add `.socratic/` to `.gitignore` unless the human chose to commit their state (`commit_state: true`). Done when `git check-ignore .socratic/config.yml` matches the choice.

6. **Hook.** If `gate` is `strict`, install `../hooks/pre-commit` as `.git/hooks/pre-commit` (executable). If a pre-commit hook already exists, keep it and call ours from it. If `gate` is not `strict`, leave hooks alone: the hook is a no-op outside strict mode anyway. Done when a strict repo blocks a commit that has no `/approve` pass.

7. **Report.** List the files written, the gate mode, and the next commands: `/socratic-tutor` to learn a concept, `/socratic-pair` to build together, `/drill` to practise review.
