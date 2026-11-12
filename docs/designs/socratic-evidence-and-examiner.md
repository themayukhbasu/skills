# Socratic evidence log and examiner bot

* **Author:** mb0850
* **Date:** 2026-11-12
* **Status:** Concept brief. Two goldfish reviews: the first raised blocking objections and the brief was revised; in the second, all seven reviewers returned "survives" with no blocking findings, and their notes are folded into the open items. Review notes left on the pull request were then adopted (see "Review notes on the pull request"); no goldfish reviewer has read those changes or the long-term goal section. Not a design, and nothing is built. The next step is a charting session that turns this into decisions and tickets.

## Overview

The socratic pack teaches by questioning. It runs in two places:

- as **repo skills** in a coding agent, with learner state in `.socratic/` files;
- as a **chat bot** (Learn: Tutor, on Grok) that teaches any topic from a Notion "To Learn" list and keeps state in Notion.

The owner's long-term aim is a persistent record of what they know, with a confidence level per concept, that other apps can read. This brief covers a first spike towards it. The owner is the only test subject.

**The problem.** The pack stores verdicts only: `unknown`, `shaky` or `solid`, plus a one-line note. The question, the learner's answer, the hints and the grader's reasoning are lost when the chat ends. So no later method can re-judge the evidence. The verdict also comes from the bot that taught, in the same conversation, and nothing outside that conversation checks it.

**The spike question.** Can the tutor and a cold re-ask leave a trail that is complete enough to re-judge later, and what does that data look like?

The spike does not claim to show whether tutor grades predict later recall. The first review showed the data cannot carry that claim (see Analysis).

**The proposal.**

```
 Learn: Tutor ──────────► evidence log (tutor records)
   teaches, hints            repo skills: git-ignored file in .socratic/
   no spaced re-asks         bot: Notion

 Examiner bot ──────────► evidence log (examiner records)
   own profile               its own Notion store
   finds taught items
   cold re-ask, no hints     never writes the tutor's fields
```

1. **One evidence-record shape, defined in the pack.** Each graded exchange is kept word for word. Repo skills write to a git-ignored file in `.socratic/`. The bot's records go to a dedicated Notion database, one row per exchange, linked to the To Learn item. Whether the tutor writes its own records or a separate recorder writes them from the session transcript is open (item 9).
2. **A separate examiner bot takes over all re-asks.** It has its own profile and skill. It finds taught items in the list without any handoff from the tutor. The tutor bot drops its re-ask rule. Each bot pokes on its own schedule.
3. **The examiner never writes the tutor's fields.** It logs to its own Notion database. After a failed cold test it asks the owner whether they want the tutor to reteach the topic, so the owner is the feedback path. Automatic feedback to the tutor is deferred.
4. **The existing levels stay as written.** The log sits beside `unknown`, `shaky` and `solid`; it does not replace them.
5. **The bot reads the pack at a fixed commit**, not from `main`. The pack can then change, including taking the spaced re-ask out of the tutor skill and `next`, without altering the live bot until its pinned commit is moved on purpose.
6. **Every record carries that commit id** as its pack version.

## Long-term goal

This section is context for any agent or person working from this brief. It says where the work is heading, in the owner's terms. **None of it is in scope for the spike.** Use it to judge whether a choice keeps the direction open; do not build towards it without a later brief.

**The idea.** A personal tutor that helps the owner build intuition, and at the same time keeps a live evaluation of what they know: what they are good at, what needs work, and how confident the record is in each.

```
 existing workflows ─┐
 (PRs, repos,        ├─► evidence ─► scoring ─► record: concept → level,
  reading)           │                          confidence, evidence behind it
 tutor bots ─────────┘                                    │
                                                          ▼
                                                    other apps
```

What the owner wants from it:

- **A live evaluation.** It updates as the owner works and learns; it is not a one-off test.
- **It plugs into existing workflows** and builds from them, instead of asking for separate study time only.
- **A knowledge graph**, with evaluation data on each node.
- **Persistent and reusable.** Other apps can read it. One the owner has in mind shows their current state to recruiters.
- **More than text later.** Audio and video signals are a possible future input. Text comes first.

**The scoring model is the centre of the idea, and it is unsolved.** The owner expects it to combine several signals and more than one model's judgement. They want it reached through experiments on collected data, with themselves as the first subject, not through introspection. The pack is expected to carry those experiments and the methods for collating the data.

**In about three months,** the owner wants the socratic bots to work as a personal tutor team: it keeps their skills from fading, and it stays interesting and fun to use. More than one bot is expected.

**Why the owner is building it,** in their order: to help themselves learn, to help other people, and to build their presence in AI. Whether other people want a tutor bot is unknown; the owner treats the work as an attempt that is worth the experience either way.

**How the pack is meant to be used once published:**

- **Repo skills** for dedicated learning inside a repo.
- **Bots** for day-to-day learning on any topic, which may be someone's main way to learn.
- **More than one vendor.** Grok today; Claude, Meta and OpenAI bots later, with roles defined once in the pack and mapped to each vendor.

**What this means for the spike.** The spike keeps evidence because a scoring model can only be built, and later changed, if the raw exchanges exist. A choice in the spike that discards evidence, ties the record to one vendor or one store, or makes the bots unpleasant to use works against the goal.

## Analysis

### What the first review found, and what changed

Seven goldfish reviewers read the first version. Their blocking objections and the response:

| Objection | Response in this version |
|---|---|
| The spike asked "do tutor grades predict cold results?" but every taught item is `solid`, so there is nothing to compare. No metric, sample size or stop rule. | The question is narrowed to "can we capture and re-test, and what does the data look like". No prediction claim is made. |
| The sample is about 10 to 15 topics in three months, and a failed cold test reopens the topic and spoils later tests. | The examiner never reopens a topic itself; reteaching happens only if the owner asks for it. No sample-size claim is made. |
| The examiner duplicates re-asks that already exist in the tutor, `next`, the drill and the bot's picking rule. | The examiner replaces the bot's re-ask; it is not added beside it. The repo skills are an open item (below). |
| The examiner is not independent of the tutor. | Accepted in part. See "The examiner's judgement" below. |
| Verbatim answers are personal data and the pack repo is public. | The repo-side log is git-ignored. The bot-side log is in the owner's private Notion. |
| The bot fetches pack files from `main` each session, so a pack change alters the live tutor and could change grading rules mid-spike. | The bot reads the pack at a fixed commit, and each record carries that commit id. |
| "Levels derived from the log" needs the scoring rule, which is out of scope. | Levels stay as written. |

### The examiner's judgement

The owner's position: an examiner with its own profile and skill behaves differently from the tutor even on the same model, in the way a fresh reviewer with a different brief finds what the author missed. The first review itself is an example: reviewers on the same model family, with no conversation history, found the `solid`-only problem that the ideation session had missed.

What this gives: a grader with no rapport to protect and no stake in the topic having been taught well, which never sees the teaching conversation.

What it does not give: independence on facts. Where the model holds a wrong belief about a concept, both bots share it. The examiner is a different judge, not an independent one. The spike does not rest on the examiner's grades being correct, because it makes no prediction claim; the grades are logged as evidence to be re-judged later.

### Known weak points, accepted for the spike

- **The list can stay wrong until the owner acts.** Today the bot's re-ask downgrades a failed topic to `shaky` and reopens it for teaching. That rule goes, which is a deliberate change to the live bot. After a failed cold test the examiner asks the owner whether to reteach. If the owner says no, or ignores the question, the topic stays marked `solid`.
- **Pinning needs upkeep.** The bot gets no pack fixes until its pinned commit is moved, and its skill today says to fetch from `main` every time.
- **Logging can change the tutor.** If the tutor writes its own records, the instruction to log is part of its prompt and may change how it teaches. Its "word for word" record is also its own retyping of the exchange.
- **Local data can be lost.** The repo-side log is git-ignored with no backup. The owner accepts this.
- **Two stores from the first day.** A local file and Notion. The shape is the same; collation is later work.
- **Some mornings bring two messages**, one from each bot.
- **No end date or failure condition.** The owner treats this as a spike and expects the next questions to become clear from use. The proposed order below gives a first checkpoint; the charting session should still set an end date.
- **Cold tests may make the bots less pleasant.** Frequency is a setting. A skipped test must be logged, or avoidance looks like missing data.

### Review notes on the pull request

Five notes were left on the pull request after the second goldfish review. What was done with each:

| Note | Outcome |
|---|---|
| Pin the bot to a commit instead of keeping pack changes additive | Adopted. Replaces the "additive" decision and settles the pack version for the bot. |
| Capture evidence outside the tutor, from session transcripts | Not decided. Recorded as open item 9, because it rests on facts about transcripts that have not been checked. |
| Give the evidence its own Notion database | Adopted. Whether the examiner shares it is open item 4. |
| On a failed cold test, the examiner asks the owner whether to reteach | Adopted. The examiner still never writes the tutor's fields. |
| Capture first, look at a week of records, then build the examiner | Recorded as the proposed order, for the charting session to confirm. |

### Ideal final result

Every graded exchange leaves evidence that a later method can re-judge, and a taught concept is re-tested cold without the owner having to remember to do it, at no cost to how pleasant the tutor is to use.

## Goals vs. Non-Goals

* **In-Scope Goals:**
  * Keep the evidence behind a verdict, in one shape across repo skills and the bot.
  * A separate examiner bot that re-asks taught topics cold and logs the result, including skips.
  * Define tutor and examiner as roles in the pack in vendor-neutral words, with Grok as the only mapping.
* **Out-of-Scope Non-Goals:**
  * Any claim that tutor grades predict recall.
  * The scoring algorithm and any confidence number.
  * Automatic feedback from the examiner to the tutor.
  * A knowledge graph, or any app built on the record.
  * Other vendors (Claude, Meta, OpenAI bots).
  * A weekly coach and a role-reversal mode.
  * A separate repo for the pack.
  * Recruiter-facing uses, and audio or video signals.

## Alternatives Weighed

- **Wait and use the one bot for some weeks before designing anything.** Rejected by author: the pack is under active development, and building it is valued for the experience whatever the outcome.
- **Decide what "solid" means by introspection.** Rejected by author: that yields gut feeling; collected data is preferred.
- **Design the scoring algorithm first.** Deferred: it needs data that does not exist yet.
- **Collect data in whatever shape and collate later.** Replaced by one record shape that keeps verbatim evidence.
- **Spike question "do tutor grades predict cold results?"** Dropped after review: every taught item is `solid`, so there is no comparison group. The author's reply is that with the trail kept, a comparison can later use fields that do vary, such as hints needed.
- **Examiner as a second mode of the tutor bot, or as a change to the existing re-asks.** Rejected by author: a separate profile and skill changes how an agent performs, even on the same model.
- **Examiner reopens a failed topic for the tutor.** Deferred by author: the flows stay separate. The examiner asks the owner instead.
- **Keep pack changes additive while the bot reads `main`.** Replaced after pull-request review: it conflicted with taking spaced re-asks out of the pack. Pinning the bot to a commit removes the conflict.
- **Keep evidence in the To Learn item's page body.** Replaced after pull-request review by a dedicated database: page bodies are awkward to collate, grow without limit, and sit in a list that Learn: Scout owns.
- **Commit the evidence log.** Rejected by author: `.socratic/` is git-ignored; the risk of local data loss is accepted.
- **Levels derived from the log.** Dropped after review: it needs the out-of-scope scoring rule.
- **A separate repo for the pack and its tools.** Deferred: raised by the author, not ruled out.
- **Weekly coach, role reversal, more vendors.** Not reached during ideation.
- **Cheaper routes raised by reviewers:** a manual run (re-ask about ten solid topics cold in a fresh chat and tabulate by hand); three extra Notion fields plus a one-page examiner prompt; extending the `oversight.yml` event; shortening the existing re-ask. Not taken: none of them keeps the tutor's own exchanges, which is the problem this brief starts from. The manual run remains a cheap first step the charting session can still choose.

## Key Decisions & Staging for Next Steps

Decided:

- A spike, text only, with the owner as the only subject.
- The spike question is about capture and re-testing, not prediction.
- One record shape; a git-ignored local file for repo skills, a dedicated Notion database for the bot.
- A separate examiner bot owns all spaced re-asks for the bot. It logs to its own Notion database and never writes the tutor's fields.
- After a failed cold test, the examiner asks the owner whether to have the tutor reteach.
- The bot reads the pack at a fixed commit. Records carry that commit id.
- Existing levels stay.
- Test frequency is a setting, found by use.

Proposed order, for the charting session to confirm:

1. Capture the tutor's exchanges first. This is the problem the brief starts from.
2. Look at a week of real records, and settle the record's fields from them.
3. Then build the examiner.

A week may cover only one or two topics, so the checkpoint may need to be "a set number of taught topics" instead.

Open, for the charting session:

1. **Spaced re-asks left in the pack.** The tutor skill (step 1.4), `next` and the drill (step 1.3) still re-ask a `solid` concept after a delay, and the bot reads the first two. With the bot pinned to a commit, they can be taken out of the pack without changing the live bot by surprise. Still to decide: when they come out, and what replaces them for repo use, where there is no examiner yet. Until then, the pack re-tests differently in a repo than in the bot.

   "All re-asks" means spaced re-asks, days or weeks later. The in-session "Re-ask after reading" gate and the transfer check stay with the tutor.
2. **The record's fields and format.** Reviewers asked for a record id, a schema version, a concrete append-only format, and fields that re-judging needs (rubric, difficulty, hint text). They advised dropping fields that can be derived.
3. **The concept key for the bot.** A Notion item is a topic, not a concept. A page id plus a sub-concept label was suggested.
4. **The Notion databases.** One for tutor evidence and one for the examiner, or one shared database with a `source` column. The bots' rules must change to allow the writes: today the tutor may edit only the item's own page.
5. **The examiner's questions.** Where an unseen problem comes from, how repeats are avoided, and whether a rubric is fixed when the topic is taught.
6. **After a failed cold test.** Whether the examiner explains the answer. The contract's "Explain always" says yes; a clean later test says no.
7. **Skips.** Separate outcomes for skipped, expired and declined, and a time limit.
8. **A time box**, and what the owner will look at when it ends. The proposed order gives a first checkpoint only.
9. **Who writes the tutor's records.** Either the tutor logs as it goes, or a separate recorder reads the session transcript afterwards and writes the records, which leaves the tutor's prompt alone. The second needs checking first: whether one bot can read another's transcripts, and how long they are kept. A transcript also holds the grader's reasoning only if the tutor says it aloud, and cutting a transcript into graded exchanges is itself a judgement. Also here: whether the learner is asked for confidence, and when.
10. **Where vendor mappings live** in the pack.
11. **How the examiner picks.** Which taught items, in what order, and what it may read to find them (the topic and recap, but not the teaching conversation). The tutor writes `Checked` today; with the examiner barred from the tutor's fields, it needs its own record of when an item was last tested.
12. **What "pack version" means.** Settled for the bot: the pinned commit id. Repo use still needs an answer, since the plugin's version string does not identify the exact files installed.
13. **Keeping the log out of git.** `.socratic/` is ignored by default, but setup's `commit_state` option can commit it. The evidence log needs its own ignore rule that holds whatever that option says.
14. **Failed writes.** A check that a record landed, so a lost write does not look like a missing session.
15. **Who can read the Notion databases**, since both hold verbatim answers.
