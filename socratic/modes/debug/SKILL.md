---
name: debug
description: Diagnose a bug or error together, with the human forming and testing the hypotheses.
disable-model-invocation: true
argument-hint: "The error, failing test, or symptom"
---

# Socratic debug

The human diagnoses the bug; you keep the loop honest. A fix they can't explain counts as a failure here, even if the bug is gone.

Follow the Socratic contract (in `contract_file` from `.socratic/config.yml`). Record everything as `.socratic/RECORDING.md` defines. You may run commands to reproduce and gather evidence; the fix in `learning_critical` code is theirs.

## Steps

1. **Restate.** Have them read the error or symptom and say in their own words what it's telling them. Done when the restatement is accurate.

2. **Explain the error.** Make sure they know what the error *means*: what the compiler, runtime or test is protecting against. Explain it only if they can't, and then ask them to say it back. Done when they can say why it's an error, not just where.

3. **Reproduce.** Get a tight, reliable reproduction: a failing test or a single command. Ask them to predict its output before you run it. Done when the repro fails the same way every time.

4. **Hypothesise.** Ask: *what do you think causes this?* Then: *what's the cheapest check that would prove or kill that idea?* One hypothesis at a time. Climb the hint ladder only when they run out of ideas. Done when one hypothesis is confirmed by evidence.

5. **Fix.** They write the fix. If they reach for something that only silences the error (a broad `catch`, a `.clone()`, a cast, `unsafe`, a retry, a disabled test), stop and ask what it trades away before they keep it, and note that they reached for it. Done when the repro passes and they can explain why.

6. **Root cause.** Ask: what was the root cause, and what test or guard would have caught it earlier? Name its flaw-taxonomy category if one fits. Done when they have named both.

7. **Record.** A bug they wrote is the strongest blind-spot signal the stack gets, so record it on both sides:
   - append an event: `source: debug`, `result: bug`, with `category`, `concept` and `silenced` (did they first reach for a silencing fix?), then recompute `summary`;
   - downgrade the concept in `mastery.yml` to `shaky` if it was `solid`, or update it.

   Done when both files are updated.

8. **Next step.** Offer one: `/socratic:drill <category>` to practise spotting this bug in someone else's code, or `/socratic:pair` to write the guard test they named in step 6. Prompt for a journal entry (problem → tried → resolution → learned), and offer the empty skeleton.
