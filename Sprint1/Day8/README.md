# Day 8 – Async/Await & the Event Loop

## Exercise: Async Batch Job Processor

A nightly enrichment batch processor that runs jobs **concurrently** using Python's asyncio.

---

## Project Structure

```
Day8/
├── models.py        ← typed data structures (Job, JobResult, BatchSummary)
├── processor.py     ← async logic (process_job, batch_supervisor)
├── main.py          ← creates jobs, calls supervisor, prints summary
├── pratice.py       ← practice file (core concepts explored)
├── pyproject.toml
└── README.md
```

---

## What I Learned Today

| Concept | Where used |
|---|---|
| `async def` + `await` | `process_job()` in processor.py |
| `asyncio.sleep()` | Simulates job work duration |
| `asyncio.gather()` | Runs all job tasks concurrently |
| `asyncio.create_task()` | Wraps each job as a scheduled task |
| `asyncio.Semaphore` | Caps max concurrency to N jobs at a time |
| `asyncio.wait_for()` | Cancels any job that exceeds a timeout |
| Event Loop | The engine behind `asyncio.run(main())` |

---

## Key Concepts Explained

### `asyncio.Semaphore(n)`
Acts like a **token pool** — only `n` tasks can run at the same time.
Any extra tasks wait until a slot frees up.

```python
semaphore = asyncio.Semaphore(3)

async with semaphore:    # blocks until a slot is available
    await do_work()
```

### `asyncio.wait_for(coro, timeout=3.0)`
Wraps a coroutine with a timer. If it doesn't finish in time,
it raises `asyncio.TimeoutError` and cancels the coroutine.

```python
try:
    result = await asyncio.wait_for(process_job(job), timeout=3.0)
except asyncio.TimeoutError:
    # job timed out, record failure and continue
```

---

## How to Run

```bash
python main.py
```

### Sample Output

```
Submitting 7 jobs to the batch processor...
  max_concurrency = 3   |   timeout_per_job = 3.0 s

  [OK]       job-001 (etl) done in 1.35s
  [OK]       job-002 (report) done in 2.36s
  [TIMEOUT]  job-003 (sync) TIMED OUT after 3.0s
  ...

==================================================
          BATCH RUN SUMMARY
==================================================
  Total jobs        : 7
  Successful        : 4
  Failed            : 3
  Failures by reason:
    - timeout       : 3

  Wall-clock time   : 6.50s  (concurrent)
  Sequential would  : 15.99s
  [SPEEDUP]         : 2.46x faster
==================================================
```

> LOW priority jobs sleep ~4s which exceeds the 3.0s timeout → they always fail with `timeout`.
> HIGH/MEDIUM priority jobs complete within the timeout.
