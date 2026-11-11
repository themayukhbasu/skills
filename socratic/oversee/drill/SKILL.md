---
name: drill
description: Run a code-review drill, sometimes with a planted flaw and sometimes clean, to practise overseeing agent output.
disable-model-invocation: true
argument-hint: "Optional: a flaw category or a language"
---

# Drill

You write a short piece of code that the human reviews as if an agent had produced it, then approves or rejects with a reason. Most drills hide **exactly one planted flaw**; about 1 in 4 is **clean**. The human is never told which. Real review asks "is this sound?", not "where is the flaw?", and clean drills keep the score honest about that.

Follow the Socratic contract (in `contract_file` from `.socratic/config.yml`). Categories come from [`TAXONOMY.md`](TAXONOMY.md). Record everything as `.socratic/RECORDING.md` defines.

## Steps

1. **Pick the category.** Take the first that applies:
   1. the human's argument;
   2. the first of `summary.blind_spots` in `.socratic/oversight.yml`;
   3. a concept in `mastery.yml` marked `solid` in the last two weeks that has a `category:` (a retention check on what tutor just taught);
   4. the category drilled least recently.

   Keep the category to yourself. Done when you have one taxonomy id.

2. **Clean or flawed.** Roll it: about 1 in 4 drills is clean, never more than 2 clean in a row. A clean drill still belongs to the category: it is code where that flaw would be easy to make, made correctly. Done when you know which.

3. **Pick the setting and difficulty.** Use the repo's main language and its domain (from `MISSION.md`), so the drill looks like real work here. Difficulty runs 1–3: start at 1, step up after a catch with no hints, step down after a miss. Done when you have a language, a plausible task ("a retry wrapper for the payments client") and a difficulty.

4. **Write the drill.** 15–40 lines, plus a one-line request it claims to fulfil. Then **self-check** it, and rewrite until it passes:
   - Flawed: exactly one flaw, from the chosen category, with a concrete consequence you can state in one sentence. Clean: no flaw at all, and it still *looks* like it could have one.
   - Realistic: an agent could plausibly write it, and it would pass a quick skim.
   - Not given away by naming, comments or odd formatting.
   - As subtle as the matching seed at that difficulty in [`SEEDS.md`](SEEDS.md), if that file exists.

   Done when every check holds.

5. **Present it.** Show the request and the code, then ask: *"Approve or reject? Say why."* Give no hint about the category, or about whether there is a flaw. Done when the drill is shown.

6. **Review loop.** The hint budget is 2 hints. Note whether the first answer is a **rubber stamp** ("looks fine" with no reasoning); if so, say so plainly before going on.
   - **Flawed, rejected for the planted flaw:** `caught`. Ask for the fix in words, and note whether it is right.
   - **Flawed, approved or rejected for a wrong reason:** give the next hint (L1, then L2: name the tell from the taxonomy). Once the budget is spent, reveal the flaw, its line, its consequence and its tell: `missed`.
   - **Clean, approved with a sound reason:** `clean`.
   - **Clean, rejected:** ask them to show the failure concretely. If they can't, reveal that the drill was clean and why the suspected flaw doesn't apply: `false_alarm`.
   - A real issue you didn't plant counts as a good catch; say so, and keep going.

   Done when the drill is resolved.

7. **Record** one event (`source: drill`, with `result`, `category`, `concept`, `hints`, `rubber_stamp`, `fix_ok`), then recompute `summary` as `RECORDING.md` defines. On `missed`, write or downgrade the matching concept in `mastery.yml` to `shaky`, with `category:` set. Done when the event is written and `summary` is current.

8. **Close.** One line on the tell to remember, then one next step: another drill, or `/socratic:tutor <concept>` after a miss the human couldn't explain once it was revealed.
