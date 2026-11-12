# skills

## `grok-bot/`

Bot team skills for the Grok bot roster (chief of staff + per-repo PM / builder / reviewer / researcher):

- `chief-of-staff`: Use when you are a user's chief-of-staff bot: routing their asks to other bots, tracking open items, asking them for decisions, giving an on-demand brief, a weekly reset, or an end-of-day wins recap.
- `project-pm`: Use when you are the PM and lead of a repo bot team (PM, builder, reviewer, researcher) whose work is tracked as GitHub Issues: daily queue check, assigning the next ticket, enforcing the ticket cap and line ceiling, flagging human-in-the-loop tickets and needs-owner after two review rounds, telling the owner once per verified review cycle when a reviewer has passed a bot PR, and ending every scheduled daily run with one short outcome summary to the owner.
- `project-builder`: Use when you are the builder on a repo bot team: turning an assigned GitHub ticket into a small, verified PR or stack through a cloud agent, handing it to the reviewer, and fixing review comments.
- `project-reviewer`: Use when you are the reviewer on a repo bot team: reviewing a builder's PR or stack after handoff, before the owner hears about it, and posting one COMMENT review with a pass or changes-needed verdict.
- `project-researcher`: Use when you are the researcher on a repo bot team: resolving assigned research tickets with cited findings. Tutoring belongs to a separate tutor bot when the team has one.
- `learn-tutor`: Use when you are a Socratic tutor bot teaching the owner one item at a time from a Notion learning list kept by a separate scout bot.

## `slow-wayfinder/`

Personal overlay on stock `/wayfinder`:

- `slow-wayfinder`: Overlay on stock `/wayfinder` (needs `/wayfinder`, `/to-spec`, `/to-tickets`): one question at a time, repo checkpoints, and map-only charting.

## `socratic/`

**Learn with AI agents without becoming a rubber stamp.** A skill stack where the agent teaches by asking, you write the code that matters, and you approve a diff only after showing you understand it. Start with [`socratic/README.md`](socratic/README.md). Generalized from the WalRusDB learning contract. Tracking: issue #10.

```
L5  Setup & guardrails   install contract, fence paths, hook
L3  Oversight training   approve gate, drills
L2  Modes                tutor · pair · debug
L1  Learner state        .socratic/ (mission, mastery, oversight)
L0  Core contract        core/CONTRACT.md
```

Install as a Claude Code plugin (in a terminal):

```
claude plugin marketplace add themayukhbasu/skills
claude plugin install socratic@themayukhbasu-skills
```

Or by hand (any agent): copy the whole `socratic/` folder into your skills directory. Keep it whole, because skills reach `core/` and `hooks/` by relative path. Then run `/socratic:setup` in the repo you want to learn in, and `/socratic:next` whenever you're not sure what to do.

Commands are written as the plugin exposes them (`/socratic:<skill>`). With a manual install, drop the `socratic:` prefix.

- `core/CONTRACT.md`: the shared behaviour contract (ownership, hint ladder, gates, escape hatch). Installed into a repo's `AGENTS.md`; every Socratic skill follows it.
- `core/RECORDING.md`: the one definition of how skills write `.socratic/` (concept ids, event fields, summary rules). Setup copies it into the repo.
- `setup/` → `/socratic:setup`: installs the contract (shared `AGENTS.md` or personal `CLAUDE.local.md`), seeds a concept roadmap from the mission, and creates `.socratic/` from `templates/`.
- `oversee/approve-gate/` → `/socratic:approve`: before accepting a diff, the human answers what it does, how it could fail, and how to verify it. A fresh reviewer grades the answers; misses feed `mastery.yml` and the next drill or lesson.
- `hooks/pre-commit`: in `gate: strict` mode, blocks a commit that touches `gate_paths` with at least `gate_min_lines` changed, until `/socratic:approve` has passed for exactly what is staged (`git write-tree`). `SOCRATIC_ESCAPE=1` lets it through and logs the escape. Tests: `python3 -m unittest socratic/hooks/test_pre_commit.py`.
- `oversee/drill/` → `/socratic:drill`: the agent writes a short review drill, with one planted flaw from `TAXONOMY.md` or (about 1 in 4) none, for the human to approve or reject. Drills target `blind_spots` and recently learned concepts. `SEEDS.md` sets the quality bar, by difficulty.
- `modes/tutor/` → `/socratic:tutor`: learn one concept by guided questioning, ending with a transfer problem and a recap. Picks review misses and blind spots first, then the mission roadmap.
- `modes/pair/` → `/socratic:pair`: the agent navigates and gathers evidence; the human writes the code. Sessions adapt to the concepts' mastery, and end with `/socratic:approve` on the human's own diff.
- `modes/debug/` → `/socratic:debug`: the human restates the error, forms hypotheses and writes the fix; the agent reproduces and keeps the loop honest. The root cause is logged by category, so drills target it.
- `next/` → `/socratic:next`: reads `.socratic/`, prints the summary (catch rate, blind spots, concepts by level) and proposes one next step.
