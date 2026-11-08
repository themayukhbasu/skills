# skills

## `grok-bot/`

Bot team skills for the Grok bot roster (chief of staff + per-repo PM / builder / researcher):

- `chief-of-staff`: Use when you are a user's chief-of-staff bot: routing their asks to other bots, tracking open items, asking them for decisions, giving an on-demand brief, a weekly reset, or an end-of-day wins recap.
- `project-pm`: Use when you are the PM and lead of a repo bot team (PM, builder, researcher) whose work is tracked as GitHub Issues: daily queue check, assigning the next ticket, enforcing PR limits, flagging human-in-the-loop tickets, telling the owner once per verified review cycle when a bot PR is ready for review, and ending every scheduled daily run with one short outcome summary to the owner.
- `project-builder`: Use when you are the builder on a repo bot team: turning an assigned GitHub ticket into a small, verified PR through a cloud agent, and fixing the owner's PR comments.
- `project-researcher`: Use when you are the researcher and tutor on a repo bot team: resolving assigned research tickets with cited findings, and tutoring the owner on demand with lessons saved in the repo.

## `slow-wayfinder/`

Personal overlay on stock `/wayfinder`:

- `slow-wayfinder`: Overlay on stock `/wayfinder` (needs `/wayfinder`, `/to-spec`, `/to-tickets`): one question at a time, repo checkpoints, and map-only charting.

## `socratic/`

A skill stack that trains developers to learn with AI agents and to oversee them instead of rubber-stamping their output. The agent asks rather than answers, and every approval has to be earned. Generalized from the WalRusDB learning contract. Tracking: issue #10.

```
L5  Setup & guardrails   install contract, fence paths, hook
L3  Oversight training   approve gate, drills
L2  Modes                tutor · pair · debug
L1  Learner state        .socratic/ (mission, mastery, oversight)
L0  Core contract        core/CONTRACT.md
```

- `core/CONTRACT.md`: the shared behaviour contract (ownership, hint ladder, gates, escape hatch). Installed into a repo's `AGENTS.md`; every Socratic skill follows it.
- `setup/` → `/socratic-setup`: installs the contract into a repo's `AGENTS.md` and creates `.socratic/` (config, mission, mastery, oversight) from `templates/`.
- `oversee/approve-gate/` → `/approve`: before accepting an agent diff, the human answers what it does, how it could fail, and how to verify it. Results are logged to `.socratic/oversight.yml`.
- `hooks/pre-commit`: in `gate: strict` mode, blocks a commit until `/approve` has passed for that exact staged diff. `SOCRATIC_ESCAPE=1` lets it through and logs the escape. Tests: `python3 -m unittest socratic/hooks/test_pre_commit.py`.
- `oversee/drill/` → `/drill`: the agent writes code with one planted flaw from `TAXONOMY.md` for the human to catch. Drills target the learner's `blind_spots`; `SEEDS.md` sets the quality bar.
- `modes/tutor/` → `/socratic-tutor`: learn one concept by guided questioning, ending with a transfer problem and a recap. Updates `mastery.yml`.
