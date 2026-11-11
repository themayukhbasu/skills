# Socratic: launch kit

Draft copy for announcing the stack. Edit freely; the voice should be yours. Anything in `[brackets]` is a number or detail only you have, so fill it from real use or cut the sentence.

## Positioning

- **For:** junior and mid-level developers who use coding agents daily.
- **Problem:** agents write faster than people review, so approval turns into a reflex and learning stops.
- **Promise:** learn with AI agents without becoming a rubber stamp.
- **How:** the agent asks, you write the code that matters, and you earn each approval.
- **Why this one:** it's one connected stack with a record of what you miss, it's plain files in your repo, and it isn't tied to one vendor's learning mode.

## One-liners

Pick one and use it everywhere (repo description, plugin description, post openers).

1. Learn with AI agents without becoming a rubber stamp.
2. Your agent writes the code. Can you say how it fails?
3. A skill stack that makes your coding agent teach you, and makes you earn every "looks good".

## Before you post

Posts with your own evidence travel much further than posts with a pitch. Use the stack for two weeks first, then have these ready:

- [ ] Your own numbers: drills done, catch rate at the start and now, your top blind spot.
- [ ] One real miss: a diff you would have approved, and what the gate made you see.
- [ ] A 60-second recording of one drill (script below).
- [ ] The install commands tested on a clean machine.

## Demo script (60 seconds, terminal recording)

1. **0–5s.** Title card: "Can you review what your agent writes?"
2. **5–15s.** Type `/socratic:drill`. The request and the code appear. Pause long enough for a viewer to read it.
3. **15–30s.** Type a confident wrong approval. The agent replies with one question.
4. **30–45s.** Type the realisation. The agent confirms and asks for the fix in words.
5. **45–55s.** Show `.socratic/oversight.yml` with the new event and the blind spot.
6. **55–60s.** End card: the one-liner and the repo URL.

Use the idempotency seed (retried charge). Nearly every viewer will approve it on first read, which is the point of the demo.

## Short post (X, Bluesky, Mastodon)

> I caught myself typing "looks good" on agent diffs I couldn't explain.
>
> So I built a skill stack that turns my coding agent into a tutor and a review coach: it asks, I write the code that matters, and I approve a diff only after saying what it does, how it fails, and how I'd verify it.
>
> [link]

Follow-up replies:

> It keeps a record of what I miss. After [N] review drills my blind spot is [category]. I'd have guessed something else.

> It's markdown, YAML and one git hook. No service, no account. Works in Claude Code today; other agents next.

## Longer post (LinkedIn, dev.to, personal blog)

**Title options**

- I was rubber-stamping my agent's code. Here's what I built to stop.
- The skill nobody is training: reviewing what your agent writes
- Learning to code when the agent already knows the answer

**Outline**

1. **The moment.** [The specific diff you approved without understanding, and what happened.]
2. **The problem in general.** Agents write faster than we review. Skimming plus green tests has become the default, and it stops both learning and oversight.
3. **The rule I started with.** On WalRusDB the agent could explain anything and write nothing that mattered. [One thing that rule taught you.]
4. **What the stack does.** The loop in one picture: learn a concept, build with it, defend the diff, drill what you missed.
5. **One drill, shown.** The retried-charge example, with the question that turns it.
6. **What my own record says.** [Your numbers and your blind spot.]
7. **What it isn't.** It's slower on purpose, it has an escape hatch, and it's v0.1 on Claude Code.
8. **Try it.** The two install commands and `/socratic:drill`.

## Show HN

**Title:** Show HN: Socratic – skills that make your coding agent teach you and test your reviews

**First comment**

> I use coding agents every day and noticed I was approving diffs I couldn't explain. This is a set of agent skills (plain markdown, plus one shell hook) built around one rule: the agent asks, and I have to earn the approval.
>
> There are three learning modes (tutor, pair, debug), an approve gate that asks what a diff does, how it could fail and how I'd verify it, and review drills with one planted flaw from a fixed list of ten categories. Results go into YAML files in the repo, so I can see which kinds of flaw I keep missing.
>
> It's v0.1 and runs on Claude Code today. The contract and the hook are agent-agnostic; the packaging isn't yet. I'd most like feedback on the flaw categories and on whether the gate is too much friction for real work.

## Words to keep and words to avoid

- **Keep:** rubber stamp, earn the approval, catch rate, blind spot, the tell.
- **Avoid:** "10x", "revolutionary", "AI-proof your career", and any claim about results you haven't measured on yourself.
