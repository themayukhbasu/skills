---
name: approve
description: Approve gate. Use before the human accepts or commits an agent-written diff, when they say "approve", "accept", "looks good", "ship it", or when a commit is blocked by the Socratic hook.
---

# Approve gate

The human may accept an agent-written diff only after showing they understand it. This gate trains **oversight**: a rubber stamp is the failure it exists to catch.

Follow the Socratic contract in `AGENTS.md`. Read `gate` from `.socratic/config.yml`; if it is `off`, say the gate is off and stop.

## Steps

1. **Fix the diff.** Default to the staged diff (`git diff --cached`), else the working-tree diff. Record its hash: `git diff --cached | sha256sum` (first 16 hex chars). Done when you know exactly which changes are under review.

2. **Ask the three questions**, all at once, and nothing else:
   1. In one line, what does this change do?
   2. Name one concrete way it could fail in production.
   3. How would you verify it works? (Which test, command or check?)

3. **Grade each answer** before you reply. Done when every answer is graded.
   - **What:** solid if it matches the diff's real behaviour, including side effects.
   - **Fail:** solid if it names a real risk *in this diff* (a mechanism, not "bugs" or "edge cases"). Check it against the flaw taxonomy if `../drill/TAXONOMY.md` exists.
   - **Verify:** solid if it names a specific test or check that would catch the failure in answer 2.

   Before grading, find the riskiest issue in the diff yourself. You grade against it, but you don't reveal it.

4. **Probe** each shaky answer with the hint ladder, starting at L1, one rung per reply. Point at the part of the diff, not at the answer. Done when all three answers are solid, or the human escapes.

5. **Record** one event in `.socratic/oversight.yml` and recompute `summary`:
   - `caught`: the human found your riskiest issue, or a real one at least as serious
   - `missed`: they passed all three answers but never found your riskiest issue. Reveal it now, with the reasoning.
   - `rubber_stamp`: their first answers were empty or generic ("looks fine", "run the tests")
   - `escape`: they said "just approve it". Note their reason.
   
   Set `category` to the taxonomy id of the riskiest issue when one fits. Done when the event is written and `summary` is current.

6. **Mark the pass.** On `caught` or `missed`, write the diff hash to `.socratic/approvals/<hash>`. The strict-mode hook checks this file. Then tell the human the gate passed. Done when the marker exists, or (for `escape`) the escape is logged.

## Grading notes

- A diff the human wrote themselves still goes through the gate when `/socratic-pair` sends it here. The questions are the same.
- Keep each reply short: one probe per turn.
- Never accept "I trust it" or "the tests pass" alone. Ask which test covers the risk.
