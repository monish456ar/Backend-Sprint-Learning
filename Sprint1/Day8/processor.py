import asyncio
import time
import random

from models import Job, JobResult, BatchSummary, FailureReason


# ── Single job processor ────────────────────────────────────────────────────

async def process_job(job: Job) -> JobResult:
    """
    Simulates processing a job.

    Duration is based on priority:
      HIGH   → sleeps ~1 s
      MEDIUM → sleeps ~2 s
      LOW    → sleeps ~4 s

    We add a small random jitter so jobs of the same priority don't
    finish at exactly the same moment (more realistic).
    """
    start = time.monotonic()

    base_duration = job.priority.value          # 1, 2, or 4 seconds
    jitter = random.uniform(0.1, 0.5)           # +0.1 – 0.5 s noise
    sleep_for = base_duration + jitter

    await asyncio.sleep(sleep_for)

    duration = time.monotonic() - start
    return JobResult(job_id=job.id, success=True, duration_seconds=duration)


# ── Batch supervisor ────────────────────────────────────────────────────────

async def batch_supervisor(
    jobs: list[Job],
    max_concurrency: int = 3,
    timeout_seconds: float = 3.0,
) -> BatchSummary:
    """
    Processes all jobs concurrently with two guardrails:

    1. Semaphore  – at most `max_concurrency` jobs run simultaneously.
    2. Timeout    – any job that exceeds `timeout_seconds` is cancelled
                    and recorded as failed; the rest of the batch continues.

    Returns a BatchSummary once every job has either completed or timed out.
    """

    # asyncio.Semaphore limits how many coroutines run at the same time.
    # Think of it as a "token pool" – grab a token to run, release when done.
    semaphore = asyncio.Semaphore(max_concurrency)

    results: list[JobResult] = []
    wall_start = time.monotonic()

    async def run_with_timeout(job: Job) -> JobResult:
        """Wraps process_job with semaphore + per-job timeout."""
        async with semaphore:                       # blocks until a slot is free
            try:
                # asyncio.wait_for cancels the coroutine if it runs too long
                result = await asyncio.wait_for(
                    process_job(job),
                    timeout=timeout_seconds,
                )
                print(f"  [OK]  {job.id} ({job.job_type.value}) done in {result.duration_seconds:.2f}s")
                return result

            except asyncio.TimeoutError:
                elapsed = timeout_seconds           # approximate; we hit the wall
                print(f"  [TIMEOUT]  {job.id} ({job.job_type.value}) TIMED OUT after {elapsed:.1f}s")
                return JobResult(
                    job_id=job.id,
                    success=False,
                    duration_seconds=elapsed,
                    failure_reason=FailureReason.TIMEOUT,
                )

    # Schedule every job as a task; gather waits for all of them.
    # Even if one times out the others keep running because the exception
    # is caught inside run_with_timeout – gather never sees it.
    tasks = [asyncio.create_task(run_with_timeout(job)) for job in jobs]
    results = await asyncio.gather(*tasks)

    wall_clock = time.monotonic() - wall_start

    # ── Build summary ───────────────────────────────────────────────────────
    successful = sum(1 for r in results if r.success)
    failed = sum(1 for r in results if not r.success)

    failures_by_reason: dict[str, int] = {}
    for r in results:
        if r.failure_reason:
            key = r.failure_reason.value
            failures_by_reason[key] = failures_by_reason.get(key, 0) + 1

    # If all jobs ran sequentially we would have waited for the sum of durations
    estimated_sequential = sum(r.duration_seconds for r in results)

    return BatchSummary(
        total_jobs=len(jobs),
        successful=successful,
        failed=failed,
        failures_by_reason=failures_by_reason,
        wall_clock_seconds=round(wall_clock, 2),
        estimated_sequential_seconds=round(estimated_sequential, 2),
    )
