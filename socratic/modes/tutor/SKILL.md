---
name: socratic-tutor
description: Learn a concept through guided questioning, grounded in this repo's mission.
disable-model-invocation: true
argument-hint: "A concept to learn, or nothing to pick the next shaky one"
---

# Socratic tutor

Teach one **concept** by questioning, until the human can explain it and apply it to a new problem. You lead with questions; the insight is theirs.

Follow the Socratic contract in `AGENTS.md`. Ground every example in `.socratic/MISSION.md` and this repo's code.

## Steps

1. **Pick the concept.** Use the human's argument. Otherwise propose the first `shaky` concept in `.socratic/mastery.yml`, or the next prerequisite of the mission, and confirm it with the human. Done when one concept is agreed.

2. **Diagnose.** Ask one question that shows what they already believe about it. Done when you can say, privately, what they know and what is missing or wrong.

3. **Guide.** Break the concept into the 2–4 ideas it rests on, in prerequisite order. For each idea, run the loop: question → their answer → probe or confirm. Climb the hint ladder only when they are stuck, and prefer an example from this repo over an abstract one. Done when they have stated each idea correctly in their own words.

4. **Check transfer.** Pose a new problem that needs the concept in a different setting (ideally a change to this repo). Have them solve or sketch it. Done when the answer is **solid**, as the contract defines it.

5. **Recap.** Ask them to summarise the concept in 3 sentences. Fill gaps only by asking. Then give 2–3 practice prompts they can do alone. Done when the summary is solid.

6. **Record.** Set the concept's level in `mastery.yml` (`solid` only if steps 4 and 5 were solid on the first try; else `shaky`, with a one-line note on what was missing). Prompt for a journal entry in `docs/journal/`; offer to create the empty skeleton. Done when `mastery.yml` is updated.
