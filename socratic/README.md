# Socratic

**Learn with AI agents without becoming a rubber stamp.**

A skill stack for developers who use coding agents every day and still want to get better at the craft. The agent teaches by asking, you write the code that matters, and you approve a diff only after showing you understand it.

```
   /socratic-tutor ──► /socratic-pair ──► /approve ───┐
     (understand)       (you build)      (you defend)  │
                             │                         ▼
                             ▼                 .socratic/ record
                      /socratic-debug        (what you know, what you miss)
                       (you diagnose)                  │
                                                       ▼
                                     /drill targets your blind spots
```

## The problem

An agent can write a working change in a minute. Reading it properly takes longer than that, so most of us skim, see green tests, and type "looks good".

That habit costs you twice:

- **You stop learning.** The agent did the thinking, and you kept the diff.
- **You stop reviewing.** Approving code you can't explain is how a double charge, a swallowed error or a missing permission check reaches production with your name on it.

More and more of the job is deciding whether to accept what an agent wrote. Almost nothing trains that directly. This stack does.

## What a session feels like

A two-minute review drill. The agent writes a short, realistic piece of code with one planted flaw and asks you to approve or reject it.

```
> /drill

Request: "Retry the charge call on network errors."

    def charge_with_retry(client, customer_id, amount, attempts=3):
        for attempt in range(attempts):
            try:
                return client.post("/charges", json={
                    "customer": customer_id,
                    "amount": amount,
                }, timeout=5)
            except (ConnectionError, TimeoutError):
                if attempt == attempts - 1:
                    raise

Approve or reject? Say why.

> approve, it retries three times and re-raises at the end

What does the server know about your first attempt when the client times out?

> ...it might have gone through. So the retry charges them twice.

That's the flaw. What would make the retry safe?
```

You get a question where another tool would give you the answer. The result goes into your record, and the categories you keep missing come back in later drills.

*(Illustrative transcript. The code is one of the seed drills in [`oversee/drill/SEEDS.md`](oversee/drill/SEEDS.md).)*

## Quick start

In Claude Code:

```
/plugin marketplace add themayukhbasu/skills
```

```
/plugin install socratic@themayukhbasu-skills
```

Then, in the repo you want to learn in:

```
/socratic-setup
```

Setup asks four questions (what you're learning, which paths are yours to write, how strict the gate is, how far hints may go) and writes your learner state to `.socratic/`.

Using another agent? Copy the whole `socratic/` folder into its skills directory. Keep it whole: the skills reach `core/` and `hooks/` by relative path.

## What's in the stack

| Command | What you do | What the agent does |
|---|---|---|
| `/socratic-tutor [concept]` | Explain a concept, then apply it to a new problem | Asks, probes, and only hints when you're stuck |
| `/socratic-pair <task>` | Write the code | Navigates, runs things, asks you to predict before each run |
| `/socratic-debug <error>` | Form and test the hypotheses, write the fix | Reproduces, and stops you before a fix that only silences the error |
| `/approve` | Say what a diff does, how it could fail, how you'd verify it | Grades your answers against the riskiest issue it found |
| `/drill [category]` | Review code with one planted flaw | Targets the flaw categories you miss most |
| `/socratic-setup` | Answer four questions | Installs the contract and your learner state |

Everything follows one shared contract, [`core/CONTRACT.md`](core/CONTRACT.md). Its main rules:

- **You own the code that teaches.** The agent writes scaffolding and leaves learning-critical paths to you.
- **Hints come one rung at a time:** a question, then a concept, then an approach in words, then a small snippet. Never the full solution.
- **Gates before progress:** explain before code, design before build, predict before run.
- **Every approval is earned.** "The tests pass" is not an answer; which test covers the risk is.

## Your record

Your progress lives in plain files in `.socratic/`, which you can read, edit and (if you choose) commit:

- `mastery.yml`: each concept you've worked on, and whether your grasp is shaky or solid.
- `oversight.yml`: every approve gate and drill, with your catch rate and your blind spots by flaw category.
- `MISSION.md`: what you're learning and why, so examples come from your own project.

Drills use ten flaw categories, each with a reviewer's tell, in [`oversee/drill/TAXONOMY.md`](oversee/drill/TAXONOMY.md): off-by-one, null and empty input, idempotency, concurrency, auth, swallowed errors, resource leaks, injection, wrong spec, and untested paths.

## Built for real work

- **There's always an escape hatch.** Say "just do it" during an outage or a deadline and the agent helps directly. The escape is logged and never blocked.
- **You choose the strictness.** `strict` blocks a commit until `/approve` passes for that exact diff. `nudge` only asks. `off` turns the gate off.
- **No service, no account, no telemetry.** It's markdown, YAML and one POSIX shell hook, all in your repo.
- **Agent-agnostic by design.** The contract installs into `AGENTS.md`, and the skills are plain markdown.

## Status

Version 0.1. Built and validated on Claude Code first. The contract and the git hook don't depend on any one agent; the plugin packaging and the slash commands do, and support for other coding agents is the next step. If you try it elsewhere, an issue saying what broke is the most useful thing you can send.

## Where it came from

This started as the learning contract for WalRusDB, a storage engine built to learn database internals and Rust, where the rule was that the agent could explain anything and write nothing that mattered. The rule worked well enough to be worth making generic.

## FAQ

**Won't this slow me down?**
Yes, on purpose, and only where you asked it to. You pick the paths that are learning-critical and how strict the gate is. Everything else, and anything you escape, runs at normal speed.

**I'm not a beginner. Is this for me?**
The tutor mode helps most when a topic is new. The approve gate and the drills are aimed at anyone who reviews agent output, which is most working developers now.

**Can I use it in a team repo?**
Today the contract installs into `AGENTS.md`, which is shared, so it suits a repo you own. A per-user install for shared repos is planned.

**Does the agent ever just give me the answer?**
When you escape, or when you reach the top of the hint ladder, it gives you a small snippet with the reasoning. It doesn't give you the full solution to something you set out to learn.
