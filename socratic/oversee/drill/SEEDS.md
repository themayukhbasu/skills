# Drill seed bank

Hand-checked examples that set the **quality bar** for generated drills: one flaw (or none), realistic, and given away by nothing on the surface. `/socratic:drill` matches their subtlety at the chosen difficulty; it does not reuse them verbatim unless the human asks for a seed.

- **Flawed seeds:** one per taxonomy category, tagged with a **difficulty** from 1 (a careful skim finds it) to 3 (needs a trace or a re-read of the request).
- **Clean seeds:** at the end. No flaw, but each looks like it could have one. They set the bar for clean drills, where the right answer is "approve, because…".

Each seed shows the request and the code. The answer key is folded under it, so the file can be read without spoiling the drills.

---

## `off-by-one` (Python) · difficulty 1

**Request:** "Split a list into pages of `size` items."

```python
def paginate(items, size):
    pages = []
    count = len(items) // size + 1
    for i in range(count):
        pages.append(items[i * size:(i + 1) * size])
    return pages
```

<details><summary>Answer key</summary>

- **Flaw:** line 3. When `len(items)` is an exact multiple of `size`, `+ 1` adds an empty last page.
- **Consequence:** the UI shows a blank "page 5 of 5".
- **Tell:** trace the case `len(items) == size`.
- **Fix:** use ceiling division, `(len(items) + size - 1) // size`.

</details>

---

## `null-empty` (TypeScript) · difficulty 1

**Request:** "Return the average order value for a customer."

```ts
export function averageOrderValue(orders: Order[]): number {
  const total = orders.reduce((sum, o) => sum + o.amount, 0);
  return total / orders.length;
}
```

<details><summary>Answer key</summary>

- **Flaw:** line 3. A customer with no orders gives `0 / 0`, which is `NaN`.
- **Consequence:** `NaN` propagates into dashboards and comparisons silently.
- **Tell:** ask what happens when the input is empty.
- **Fix:** return `0` (or `null`) explicitly when `orders.length === 0`, and decide which with the caller.

</details>

---

## `idempotency` (Python) · difficulty 2

**Request:** "Retry the charge call on network errors."

```python
def charge_with_retry(client, customer_id, amount, attempts=3):
    for attempt in range(attempts):
        try:
            return client.post("/charges", json={
                "customer": customer_id,
                "amount": amount,
            }, timeout=5)
        except (ConnectionError, TimeoutError):
            if attempt == attempts - 1:
                raise
```

<details><summary>Answer key</summary>

- **Flaw:** line 4. A timeout does not mean the charge failed; the retry can charge twice. No idempotency key is sent.
- **Consequence:** customers are double-charged during slow network periods.
- **Tell:** a retried non-idempotent `POST`.
- **Fix:** generate one idempotency key before the loop and send it on every attempt.

</details>

---

## `concurrency` (Go) · difficulty 3

**Request:** "Cache user profiles in memory."

```go
type Cache struct {
	mu    sync.Mutex
	items map[string]Profile
}

func (c *Cache) Get(id string, load func(string) Profile) Profile {
	c.mu.Lock()
	p, ok := c.items[id]
	c.mu.Unlock()
	if !ok {
		p = load(id)
		c.items[id] = p
	}
	return p
}
```

<details><summary>Answer key</summary>

- **Flaw:** line 12. The map write happens after the lock is released.
- **Consequence:** concurrent misses race on the map; Go panics with "concurrent map writes".
- **Tell:** check every access to shared state is under the lock.
- **Fix:** take the lock again for the write (and re-check), or hold it across the load if the load is cheap.

</details>

---

## `auth` (TypeScript, Express) · difficulty 1

**Request:** "Let users delete their own comments."

```ts
router.delete("/comments/:id", requireLogin, async (req, res) => {
  const comment = await db.comments.findById(req.params.id);
  if (!comment) return res.status(404).end();
  await db.comments.delete(comment.id);
  res.status(204).end();
});
```

<details><summary>Answer key</summary>

- **Flaw:** line 4. It checks that someone is logged in, but not that they own the comment.
- **Consequence:** any user can delete anyone's comment.
- **Tell:** find where ownership is enforced. Here it isn't.
- **Fix:** return 403 unless `comment.authorId === req.user.id`.

</details>

---

## `error-swallow` (Python) · difficulty 2

**Request:** "Load feature flags from the config service; fall back gracefully."

```python
def load_flags(client):
    try:
        resp = client.get("/flags")
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return {}
```

<details><summary>Answer key</summary>

- **Flaw:** lines 6–7. Every error, including bad JSON and auth failures, quietly becomes "all flags off", with no log.
- **Consequence:** a config outage silently disables features in production, and nobody is alerted.
- **Tell:** follow the `except`: where does the failure go?
- **Fix:** catch only network errors, log them, and fall back to the last known good flags rather than `{}`.

</details>

---

## `resource-leak` (Python) · difficulty 2

**Request:** "Count lines in a log file that contain ERROR."

```python
def count_errors(path):
    f = open(path)
    count = 0
    for line in f:
        if "ERROR" in line:
            count += 1
    f.close()
    return count
```

<details><summary>Answer key</summary>

- **Flaw:** line 2. If iteration raises (for example a decode error), `f.close()` never runs.
- **Consequence:** a batch job over thousands of files runs out of file descriptors.
- **Tell:** is every open paired with a close on the error path?
- **Fix:** `with open(path) as f:`.

</details>

---

## `injection` (Python, SQL) · difficulty 1

**Request:** "Search products by name."

```python
def search_products(conn, term):
    sql = f"SELECT id, name FROM products WHERE name ILIKE '%{term}%'"
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()
```

<details><summary>Answer key</summary>

- **Flaw:** line 2. User input is formatted straight into SQL.
- **Consequence:** `term = "'; DROP TABLE products; --"` runs as SQL.
- **Tell:** trace user input to the interpreter it reaches.
- **Fix:** a parameterized query, `cur.execute("... ILIKE %s", (f"%{term}%",))`.

</details>

---

## `wrong-spec` (TypeScript) · difficulty 3

**Request:** "Show users whose trial ends in the next 7 days, so we can email them."

```ts
export function trialsEndingSoon(users: User[], now: Date): User[] {
  const week = 7 * 24 * 60 * 60 * 1000;
  return users.filter(
    (u) => u.trialEndsAt.getTime() - now.getTime() <= week
  );
}
```

<details><summary>Answer key</summary>

- **Flaw:** line 4. It has no lower bound, so already-expired trials (negative difference) are included.
- **Consequence:** churned users get "your trial ends soon" emails.
- **Tell:** re-read the request and test a value outside the intended range.
- **Fix:** also require the difference to be `>= 0`.

</details>

---

## `untested-path` (Python) · difficulty 2

**Request:** "Apply a discount code; codes can be percentage or fixed amount. Add tests."

```python
def apply_discount(total, code):
    if code.kind == "percent":
        return round(total * (1 - code.value / 100), 2)
    return max(total - code.value, 0)


def test_percent_discount():
    assert apply_discount(100, Code("percent", 10)) == 90


def test_percent_discount_rounds():
    assert apply_discount(9.99, Code("percent", 15)) == 8.49
```

<details><summary>Answer key</summary>

- **Flaw:** the fixed-amount branch (line 4) has no test. Both tests exercise the percent path only.
- **Consequence:** a regression in fixed discounts ships green.
- **Tell:** for each branch, which test makes it run?
- **Fix:** add tests for a fixed discount, and for a fixed discount larger than the total.

</details>

---

# Clean seeds

## clean: `idempotency` (Python) · difficulty 2

**Request:** "Retry the charge call on network errors."

```python
def charge_with_retry(client, customer_id, amount, attempts=3):
    key = str(uuid.uuid4())
    for attempt in range(attempts):
        try:
            return client.post("/charges", json={
                "customer": customer_id,
                "amount": amount,
            }, headers={"Idempotency-Key": key}, timeout=5)
        except (ConnectionError, TimeoutError):
            if attempt == attempts - 1:
                raise
```

<details><summary>Answer key</summary>

- **Clean.** The key is generated once, before the loop, and sent on every attempt, so the server deduplicates a retried charge.
- **What a reviewer might wrongly flag:** "the POST is retried". That's safe here, because of the key.
- **Good approval reason:** names the key and why it must be created outside the loop.

</details>

---

## clean: `off-by-one` (Python) · difficulty 1

**Request:** "Split a list into pages of `size` items."

```python
def paginate(items, size):
    pages = []
    for start in range(0, len(items), size):
        pages.append(items[start:start + size])
    return pages
```

<details><summary>Answer key</summary>

- **Clean.** `range(0, len, size)` stops before `len`, and slicing past the end is safe in Python, so there is no empty last page and no lost items. An empty list gives `[]`.
- **What a reviewer might wrongly flag:** "`start + size` can run past the end". Slices clamp.
- **Good approval reason:** traces the exact-multiple case and the empty case.

</details>

---

## clean: `auth` (TypeScript, Express) · difficulty 1

**Request:** "Let users delete their own comments."

```ts
router.delete("/comments/:id", requireLogin, async (req, res) => {
  const comment = await db.comments.findById(req.params.id);
  if (!comment || comment.authorId !== req.user.id) {
    return res.status(404).end();
  }
  await db.comments.delete(comment.id);
  res.status(204).end();
});
```

<details><summary>Answer key</summary>

- **Clean.** Ownership is checked before the delete. Returning 404 rather than 403 for someone else's comment is a deliberate choice: it doesn't reveal that the comment exists.
- **What a reviewer might wrongly flag:** "it should be 403". That's a style choice, not a flaw.
- **Good approval reason:** points at the ownership check and says who can reach the delete.

</details>
