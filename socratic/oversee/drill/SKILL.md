---
name: drill
description: Run a code-review drill with one planted flaw, to practise overseeing agent output.
disable-model-invocation: true
argument-hint: "Optional: a flaw category or a language"
---

# Drill

You write a short piece of code with **exactly one planted flaw**. The human reviews it as if an agent had produced it, then approves or rejects it with a reason. Drills train the eye that `/approve` relies on.

Follow the Socratic contract in `AGENTS.md`. Categories come from [`TAXONOMY.md`](TAXONOMY.md).

## Steps

1. **Pick the category.** Use the human's argument if they gave one. Otherwise take the first of `summary.blind_spots` in `.socratic/oversight.yml`. If that is empty, take the category least recently drilled. Keep the category to yourself. Done when you have one taxonomy id.

2. **Pick the setting.** Use the repo's main language and its domain (from `MISSION.md`), so the drill looks like real work here. Done when you have a language and a plausible task ("a retry wrapper for the payments client").

3. **Write the drill.** 15–40 lines, plus a one-line request it claims to fulfil. Then **self-check** it, and rewrite until it passes:
   - Exactly one flaw, from the chosen category, and nothing else wrong.
   - Realistic: an agent could plausibly write it, and it would pass a quick skim.
   - Not given away by naming, comments or odd formatting.
   - The flaw has a concrete consequence you can state in one sentence.
   - About as subtle as the matching example in [`SEEDS.md`](SEEDS.md), if that file exists.

   Done when every check holds.

4. **Present it.** Show the request and the code, then ask: *"Approve or reject? Say why."* Give no hint about the category. Done when the drill is shown.

5. **Review loop.** The hint budget is 2 hints.
   - **Rejected for the planted flaw:** `caught`. Ask them for the fix in words.
   - **Approved, or rejected for a wrong reason:** give the next hint up the ladder (L1, then L2: name the tell from the taxonomy). Once the budget is spent, reveal the flaw, its line, its consequence and its tell.
   - **"Looks fine" with no reasoning:** `rubber_stamp`. Say so plainly, then give hint 1.
   - A real issue you didn't plant counts as a good catch; say so, and keep going toward the planted one.

   Done when the flaw is caught or revealed.

6. **Record** one event in `.socratic/oversight.yml` (`source: drill`, `result`, `category`) and recompute `summary`. A category missed 2 or more times in the last 10 events goes into `blind_spots`; a category caught 3 times in a row comes out. Done when the event is written.

7. **Close.** One line on the tell to remember, and offer another drill.
