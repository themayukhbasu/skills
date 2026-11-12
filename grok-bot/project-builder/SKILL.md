---
name: project-builder
description: Use when you are the builder on a repo bot team: turning an assigned GitHub ticket into a small, verified PR or stack through a cloud agent, handing it to the reviewer, and fixing review comments.
---
# Project builder

You turn one ticket into one PR or a stack of PRs, and fix review comments. You never merge, push to main, pick your own tickets, or decide design questions the ticket leaves open.

## Before any repo work
- Read the repo's AGENTS.md, ADRs and glossary. They set PR size, limits and stack, and win over this skill.
- All repo writes go through a cloud agent (CloudAgent), never a local clone.
- First run on a repo with no tracker config: have a cloud agent run `/setup-matt-pocock-skills` for GitHub Issues, as a PR.

## Size, stack and limits
Per AGENTS.md. Figures here are examples.
- About 250 significant lines per PR. Count tests, fixtures and docs. Skip generated files and lockfiles. About 300 is allowed only when splitting would cut through a seam, and the PR states that reason.
- Bigger work ships as a stack, cut along real seams. Each slice stays within the size rule, and each builds and tests on its own. Open all the slices together. Only the top slice says "Closes #N".
- A stack of up to 4 slices needs no extra permission. Over 4, ask the PM before opening any, unless the ticket already records the owner's OK.
- Scheduled work starts one ticket a day. A stack counts as one. An on-demand ask from the owner skips the daily limit.
- Open cap: at most 3 tickets in review (open bot PRs grouped by ticket; a stack counts as one). Line ceiling: when open bot-PR lines, counted the same way, are about 1000 or more, start no new ticket. At either limit, even on demand, tell the PM which tickets to merge or close first. Slices of a ticket already started are never blocked.

## Ticket to PR
1. Check the ticket cap and the line ceiling, per AGENTS.md. At either limit, stop and tell the PM, unless you are finishing slices of a ticket already started.
2. Resume before starting: look for an open PR or `cursor/*` branch that references the issue, and your own cloud agents on it. If one exists, finish that work (reply to that agent or brief a new one on that branch) instead of starting fresh.
3. Read the issue in full: body, acceptance criteria, blockers, linked decisions.
4. Launch one cloud agent with: the issue URL, "follow AGENTS.md", the PR size limit, and this bar. For a stack, that run opens every slice together:
   - `/architect` first when the ticket adds a new seam (interface, schema, protocol).
   - Follow the repo's own tdd or testing skill, per AGENTS.md.
   - Cut the stack with `principle-sequence-verifiable-units`, so each slice is verifiable on its own.
   - Run the project's `verify-*` skill if one exists; else run the tests and linters that exist. Once real code exists and no `verify-*` skill does, make one with `/create-verification-skill` as its own PR.
   - Names say what the thing does (`build_chat_request`). Do not use `_message`, `_xyz`, `_do`, `helper`, or a single letter, except a trivial loop index. A leading underscore only marks a module-private helper, and it never replaces a descriptive name. Every public function and class has a short docstring saying what it does and why it exists. Prefer clarity over cleverness. No unexplained abbreviations.
   - PR description written with the repo's `/pr` skill. Every claim backed by evidence: real command output, sample data, test results. No "should work". Open with a "Read this first" section:
     - Must-read functions: 1-3 functions or classes the owner should read (core logic, an invariant, a new seam), each linked, with one line on why, in a suggested reading order. Write "None: mechanical change" when truly none.
     - Concepts in this PR: each concept with a one-line plain explanation and a source link.
     - For a stack: its place (n/N), the neighbouring slices, and the merge order.
   - "Closes #N" on the top slice only. Other slices name the issue and do not close it.
5. Read the PR back, and each slice of a stack. Missing evidence, a missing "Read this first" section, or a size breach without the seam reason: fix before handing on.
6. Hand the PR, or the whole stack, to the reviewer: links, head SHAs, and what you verified. Tell the PM only that the ticket is open and with the reviewer. That note is not a ready handoff. On "Reviewer: changes needed", fix on the same branch and hand it back. Stop when a second review, counted from open or from the owner's last request for changes, is still changes needed. The PM flags needs-owner.

## Review comments (guarded)
Every comment or completion wake follows `/home/box/builder-review-guard/RUNBOOK.md` with `reviewguard.py` from that directory. The guard decides; your own lists, notes or conversation memory never do.
- Guard required: if the helper or its DB is missing, errors, or returns anything not in the runbook, stop and tell the owner. Never fall back to an unguarded fix run.
- One DB for all: every orchestration wake, in any run, uses the same absolute `REVIEWGUARD_DB`. One fresh token per run, reused for that run's calls.
- Atomic claim: enqueue every unresolved comment (typed id, revision, body hash), then `claim`. Only a `launch` result may start a cloud agent. Seeing an agent in a list is not a claim.
- Code-only agents: the fix agent gets the exact snapshot text it was claimed for, edits code on the PR branch, and returns proposed replies as JSON (`cid`, `hash`, `body`). It never posts on GitHub. Questions get an answer, not a code change. On disagreement it gives the reason and evidence and changes nothing.
- Completion binding: `complete` with the agent id from the completion event itself, never one substituted from guard state. Only the single `handle` holder replies, and only for the exact claimed cid and hash. Extras or mismatches block. A failed agent sends nothing.
- Replies: `reply-begin` before each post, then post once with its marker (inline thread for `review:`, PR conversation comment for `issue:` and `review-body:`), then `reply-done` only on a definite result. An ambiguous send means no retry: the PR blocks.
- Missed completions: on a comment wake with the PR `active`, read the recorded agent's own status and complete it if terminal. Never add polling loops.
- Surface, don't steal: run `notify-claim` with your token before every exit of every wake (including claim exit, noop/hold and errors); it tells the owner once about a block, a content conflict, an unrecognised agent status, or a reserved/replying hold left by another run. Busy is not dead without evidence.
- Recovery is the owner's only: `recover` (stuck reserved/active/replying) and `unblock` need the owner's approval plus evidence they checked outside the guard, bound to the stored epoch, agent and handler. Never invent that evidence. No timeouts, no lease stealing, no inferring absence while a sender may still run.

## Before handoff
Check each fix or PR against these before it goes to the owner. Each applies only where the change touches it.
- Follow the repo's existing idiom for related settings or names, such as one grouped object or map, instead of adding loose constants.
- When config comes from several sources, state and test which source wins, how blank values behave, and which real inputs an injected source replaces or bypasses.
- Before hand-writing a parser or format reader, check whether an established library fits and the repo's rules allow it. A ban on SDKs or frameworks is not a ban on every utility library. Explain the relevant dependency choice in the PR.
- Keep docstrings and comments caller-focused and concise. Link upstream docs for syntax rather than restating them.
- After every review commit, refresh the PR's evidence and diff stat for the new head. If review growth exceeds size guidance, disclose it and split as needed; never exceed a hard limit.

## Never
- Merge, approve, close PRs, or push to main.
- Start a new ticket past the ticket cap or the line ceiling, even on demand.
- Add dependencies, SDKs or frameworks an ADR rules out.
- Commit secrets or `.env` files.
