# Recording learner state

<!-- Copied into .socratic/RECORDING.md by /socratic:setup. The single source for how every Socratic skill writes .socratic/. -->

Every skill that records anything follows this file. Record **as each gate is graded**, so a session that stops early still leaves its evidence.

## Concepts: `.socratic/mastery.yml`

```yaml
concepts:
  idempotent-retries:      # id: kebab-case
    level: shaky           # unknown | shaky | solid
    category: idempotency  # optional: a flaw-taxonomy id this concept protects against
    source: approve        # who last wrote it: mission | tutor | pair | debug | approve | drill
    updated: 2026-11-11    # last write
    checked: 2026-11-11    # last time a gate tested it (for staleness)
    note: missed POST retried on timeout
```

- **Id:** kebab-case, named after the idea, not the code (`root-split`, not `split_root_fn`). Reuse an existing key before adding one.
- **unknown:** written only by setup, from the mission roadmap. A concept is `unknown` until a gate tests it.
- **shaky:** a gate found something missing. Write it as soon as the gap shows, and say what was missing in `note`.
- **solid:** the human named the invariant, said why it matters and traced a failure, on the first try.
- **Downgrade** a `solid` concept to `shaky` when a review miss or a debug root cause lands on it.

## Events: `.socratic/oversight.yml`

Append one event per graded review. Fields beyond `date`, `source` and `result` are optional; write them whenever you know them.

```yaml
events:
  - date: 2026-11-11
    source: approve        # approve | drill | debug | escape
    author: agent          # approve only: agent (reviewing agent code) | human (defending own code)
    result: caught         # see the table below
    rubber_stamp: false    # approve and drill: were the first answers empty or generic?
    category: idempotency  # flaw-taxonomy id, when one fits
    concept: idempotent-retries  # the mastery.yml key this touches
    hints: 1               # hints used before the outcome
    fix_ok: true           # drill: was the fix-in-words right?
    silenced: false        # debug: did the human first reach for a fix that only hides the error?
    note: one line
```

| source | result | meaning |
|---|---|---|
| approve | `caught` | found the riskiest issue, or a real one as serious |
| approve | `missed` | never found it; it was revealed |
| approve | `clean` | no serious issue existed, and the human justified approving |
| drill | `caught` / `missed` | as above, for the planted flaw |
| drill | `clean` | approved a clean drill, with a reason |
| drill | `false_alarm` | rejected a clean drill |
| debug | `bug` | a bug the human wrote, with its root-cause `category` |
| escape | `escape` | a gate or hook was skipped on purpose; `note` holds the reason |

## Recompute the summary

Run this after appending events. Every skill that writes `oversight.yml` uses these rules and no others.

1. **Fold escapes.** Turn each line of `.socratic/escapes.log` (`time  hash  reason`) into an `escape` event, then empty the log.
2. **Window:** the last 20 review events written by `approve` with `author: agent`, or by `drill`.
3. **catch_rate** = caught / (caught + missed) in the window. `null` when the denominator is 0.
4. **false_alarm_rate** = false_alarm / (false_alarm + clean), over drill events in the window.
5. **own_code_catch_rate:** as `catch_rate`, over the last 20 `approve` events with `author: human`.
6. **rubber_stamps:** count of `rubber_stamp: true` in the window. **escapes:** count of all `escape` events.
7. **blind_spots:** a category enters when it shows up 2 or more times in its last 10 events as `missed` or `bug`. It leaves after 3 `caught` in a row in that category. Order by most recent miss.
