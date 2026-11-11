---
name: approve
description: Approve gate. Use before the human accepts or commits a diff, when they say "approve", "accept", "looks good", "ship it", or when a commit is blocked by the Socratic hook.
---

# Approve gate

The human may accept a diff only after showing they understand it. This gate trains **oversight**: a rubber stamp is the failure it exists to catch, and a justified "this is fine" is a pass, not a miss.

Follow the Socratic contract (installed in `contract_file` from `.socratic/config.yml`). Record everything as `.socratic/RECORDING.md` defines. If `gate` is `off`, say the gate is off and stop.

## Steps

1. **Fix the diff.** Review exactly what will be committed:
   - `strict` mode: the changes must be **staged** before the gate starts. If nothing is staged, ask the human to stage what they mean to commit (or stage it with their OK). The id is `git write-tree`, the tree of the staged changes, which is the same id the hook computes.
   - `nudge` mode: the staged diff if any, else the working-tree diff. No id is needed.
   - Note the **author**: `agent` for a diff an agent wrote, `human` when the human wrote it (for example when `/socratic:pair` sends their diff here).

   Done when you know exactly which changes are under review, who wrote them, and (in strict mode) their tree id.

2. **Find the riskiest issue, independently.** Where the agent supports it, give the diff to a **fresh subagent** that did not write it, with the flaw taxonomy (`../drill/TAXONOMY.md`). It returns the single riskiest issue with its category, or **none** if the diff has no serious issue. Without subagents, do the review yourself, as a stranger to the diff. Keep the result to yourself. Done when you hold one issue, or none.

3. **Ask the three questions**, all at once, and nothing else:
   1. In one line, what does this change do?
   2. Name one concrete way it could fail in production, or say why it can't.
   3. How would you verify it works? (Which test, command or check?)

   Note whether the first answers are a **rubber stamp**: empty or generic ("looks fine", "run the tests"). Done when the answers are in.

4. **Grade each answer.**
   - **What:** solid if it matches the diff's real behaviour, including side effects.
   - **Fail:** solid if it names a real risk *in this diff* (a mechanism, not "bugs" or "edge cases"), or, when step 2 found none, gives a sound reason the obvious risks don't apply.
   - **Verify:** solid if it names a specific test or check that would catch the failure in answer 2.

   Done when every answer is graded.

5. **Probe** each shaky answer with the hint ladder, starting at L1, one rung per reply. Point at the part of the diff, not at the answer. Count the hints. Done when all three answers are solid, or the human escapes.

6. **Record** one event (`source: approve`, with `author`, `rubber_stamp`, `hints`, `category`, `concept`), then recompute `summary`:
   - `caught`: they found the issue from step 2, or a real one at least as serious.
   - `missed`: all three answers ended solid, but they never found the issue. Reveal it now, with the reasoning.
   - `clean`: step 2 found none, and they justified approving.
   - `escape`: they said "just approve it". Note their reason.

   On `missed`, or on a `rubber_stamp`, write or downgrade the matching concept in `mastery.yml` to `shaky`, with `category:` set. Done when the event is written and `summary` is current.

7. **Mark the pass.** When step 5 ended with all three answers solid (whatever the first answers were), write `.socratic/approvals/<tree id>` in strict mode, and tell the human the gate passed. Done when the marker exists, or (for `escape`) the escape is logged.

8. **Next step.** Offer one: after a miss, `/socratic:drill <category>` for a quick rep, or `/socratic:tutor <concept>` if they couldn't explain the mechanism after the reveal. After a catch or a clean pass, nothing: let them ship.

## Grading notes

- Keep each reply short: one probe per turn.
- Never accept "I trust it" or "the tests pass" alone. Ask which test covers the risk.
