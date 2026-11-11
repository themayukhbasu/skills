---
name: next
description: Show the learner's Socratic summary and propose one next step. Use when the human asks "what next?", "what should I work on?", or for their progress.
---

# Socratic next

Answer "what should I do now?" from the learner's own record, with one step, not a menu.

Follow the Socratic contract (in `contract_file` from `.socratic/config.yml`). If `.socratic/` doesn't exist, say so and suggest `/socratic:setup`. Record as `.socratic/RECORDING.md` defines.

## Steps

1. **Refresh.** Recompute `summary` in `.socratic/oversight.yml` as `RECORDING.md` defines. This folds `.socratic/escapes.log`. Done when `summary` is current.

2. **Show the summary**, in a few lines:

   ```
   catch rate 0.62 (last 20)   false alarms 0.10   own code 0.80
   rubber stamps 2             escapes 3 (2 new)
   blind spots: idempotency, off-by-one
   concepts: 4 solid · 3 shaky · 5 unknown
   ```

   Done when it's shown.

3. **Propose one next step**, the first that applies:

   | Condition | Next step |
   |---|---|
   | new escapes were folded | show the count and their reasons; ask if one deserves a look |
   | a blind spot is open | `/socratic:drill <category>` |
   | a concept went `shaky` from a review miss | `/socratic:tutor <concept>` |
   | a `solid` concept hasn't been `checked` for a month | a quick re-ask, here and now |
   | nothing is pending | `/socratic:tutor` on the next `unknown` roadmap concept, or `/socratic:pair` on a real task |

   Done when one step is proposed, with one line on why.
