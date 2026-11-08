# Drill seed bank

Hand-checked examples, one per taxonomy category. They set the **quality bar** for generated drills: one flaw, realistic, and given away by nothing on the surface. `/drill` matches their subtlety; it does not reuse them verbatim unless the human asks for a seed.

Each seed lists the request, the code, then the answer key. Keep the answer key out of the human's view.

---

## `off-by-one` (Python)

**Request:** "Split a list into pages of `size` items."

```python
def paginate(items, size):
    pages = []
    count = len(items) // size + 1
    for i in range(count):
        pages.append(items[i * size:(i + 1) * size])
    return pages
```

- **Flaw:** line 3. When `len(items)` is an exact multiple of `size`, `+ 1` adds an empty last page.
- **Consequence:** the UI shows a blank "page 5 of 5".
- **Tell:** trace the case `len(items) == size`.
- **Fix:** use ceiling division, `(len(items) + size - 1) // size`.

---

## `null-empty` (TypeScript)

**Request:** "Return the average order value for a customer."

```ts
export function averageOrderValue(orders: Order[]): number {
  const total = orders.reduce((sum, o) => sum + o.amount, 0);
  return total / orders.length;
}
```

- **Flaw:** line 3. A customer with no orders gives `0 / 0`, which is `NaN`.
- **Consequence:** `NaN` propagates into dashboards and comparisons silently.
- **Tell:** ask what happens when the input is empty.
- **Fix:** return `0` (or `null`) explicitly when `orders.length === 0`, and decide which with the caller.

---

## `idempotency` (Python)

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

- **Flaw:** line 4. A timeout does not mean the charge failed; the retry can charge twice. No idempotency key is sent.
- **Consequence:** customers are double-charged during slow network periods.
- **Tell:** a retried non-idempotent `POST`.
- **Fix:** generate one idempotency key before the loop and send it on every attempt.

---

## `concurrency` (Go)

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

- **Flaw:** line 12. The map write happens after the lock is released.
- **Consequence:** concurrent misses race on the map; Go panics with "concurrent map writes".
- **Tell:** check every access to shared state is under the lock.
- **Fix:** take the lock again for the write (and re-check), or hold it across the load if the load is cheap.

---

## `auth` (TypeScript, Express)

**Request:** "Let users delete their own comments."

```ts
router.delete("/comments/:id", requireLogin, async (req, res) => {
  const comment = await db.comments.findById(req.params.id);
  if (!comment) return res.status(404).end();
  await db.comments.delete(comment.id);
  res.status(204).end();
});
```

- **Flaw:** line 4. It checks that someone is logged in, but not that they own the comment.
- **Consequence:** any user can delete anyone's comment.
- **Tell:** find where ownership is enforced. Here it isn't.
- **Fix:** return 403 unless `comment.authorId === req.user.id`.

---

## `error-swallow` (Python)

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

- **Flaw:** lines 6–7. Every error, including bad JSON and auth failures, quietly becomes "all flags off", with no log.
- **Consequence:** a config outage silently disables features in production, and nobody is alerted.
- **Tell:** follow the `except`: where does the failure go?
- **Fix:** catch only network errors, log them, and fall back to the last known good flags rather than `{}`.

---

## `resource-leak` (Python)

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

- **Flaw:** line 2. If iteration raises (for example a decode error), `f.close()` never runs.
- **Consequence:** a batch job over thousands of files runs out of file descriptors.
- **Tell:** is every open paired with a close on the error path?
- **Fix:** `with open(path) as f:`.

---

## `injection` (Python, SQL)

**Request:** "Search products by name."

```python
def search_products(conn, term):
    sql = f"SELECT id, name FROM products WHERE name ILIKE '%{term}%'"
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()
```

- **Flaw:** line 2. User input is formatted straight into SQL.
- **Consequence:** `term = "'; DROP TABLE products; --"` runs as SQL.
- **Tell:** trace user input to the interpreter it reaches.
- **Fix:** a parameterized query, `cur.execute("... ILIKE %s", (f"%{term}%",))`.

---

## `wrong-spec` (TypeScript)

**Request:** "Show users whose trial ends in the next 7 days, so we can email them."

```ts
export function trialsEndingSoon(users: User[], now: Date): User[] {
  const week = 7 * 24 * 60 * 60 * 1000;
  return users.filter(
    (u) => u.trialEndsAt.getTime() - now.getTime() <= week
  );
}
```

- **Flaw:** line 4. It has no lower bound, so already-expired trials (negative difference) are included.
- **Consequence:** churned users get "your trial ends soon" emails.
- **Tell:** re-read the request and test a value outside the intended range.
- **Fix:** also require the difference to be `>= 0`.

---

## `untested-path` (Python)

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

- **Flaw:** the fixed-amount branch (line 4) has no test. Both tests exercise the percent path only.
- **Consequence:** a regression in fixed discounts ships green.
- **Tell:** for each branch, which test makes it run?
- **Fix:** add tests for a fixed discount, and for a fixed discount larger than the total.
