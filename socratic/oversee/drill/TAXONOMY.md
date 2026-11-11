# Flaw taxonomy

The fixed list of flaw categories for `/socratic:drill`, `/socratic:approve` and `/socratic:debug`. Every planted flaw and every `category` in `oversight.yml` uses one of these ids. Each has a **tell**: what a careful reviewer looks for.

| id | Flaw | Tell |
|---|---|---|
| `off-by-one` | Wrong boundary: `<` vs `<=`, the last page, an empty range | Trace the first, the last and the empty case by hand |
| `null-empty` | Missing, null or empty input not handled | Ask: what if this is empty, null or zero? |
| `idempotency` | Retrying or re-running causes a double effect | Find every retry and replay; is the operation safe twice? |
| `concurrency` | Shared state without a lock, check-then-act, ordering assumptions | Two callers at once: what interleaving breaks it? |
| `auth` | Missing or wrong permission check; trusts client input for identity | Who can call this, and where is that enforced? |
| `error-swallow` | An error is caught and ignored, or turned into a wrong default | Follow every `catch` / `except` / `_ =`: where does the failure go? |
| `resource-leak` | A file, connection, lock or listener isn't released on every path | Is every open paired with a close, including on error? |
| `injection` | Untrusted input concatenated into SQL, a shell command, HTML or a path | Trace user input to every interpreter it reaches |
| `wrong-spec` | The code works but does something different from what was asked | Re-read the request; diff the intent, not just the code |
| `untested-path` | The risky branch has no test; the tests pass by never reaching it | For each branch: which test makes it run? |

Add a category only when a real miss fits none of these, and record why in the PR that adds it.
