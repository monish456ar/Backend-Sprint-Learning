import asyncio

from models import Job, JobType, Priority
from processor import batch_supervisor


def create_jobs() -> list[Job]:
    """Define the nightly enrichment batch."""
    return [
        Job(id="job-001", job_type=JobType.ETL,     priority=Priority.HIGH,   payload={"table": "users"}),
        Job(id="job-002", job_type=JobType.REPORT,  priority=Priority.MEDIUM, payload={"report": "sales_daily"}),
        Job(id="job-003", job_type=JobType.SYNC,    priority=Priority.LOW,    payload={"source": "crm"}),
        Job(id="job-004", job_type=JobType.CLEANUP, priority=Priority.LOW,    payload={"older_than_days": 90}),
        Job(id="job-005", job_type=JobType.ETL,     priority=Priority.HIGH,   payload={"table": "orders"}),
        Job(id="job-006", job_type=JobType.REPORT,  priority=Priority.MEDIUM, payload={"report": "inventory"}),
        Job(id="job-007", job_type=JobType.SYNC,    priority=Priority.LOW,    payload={"source": "erp"}),
    ]


def print_summary(summary) -> None:
    """Pretty-print the BatchSummary."""
    print("\n" + "=" * 50)
    print("          BATCH RUN SUMMARY")
    print("=" * 50)
    print(f"  Total jobs        : {summary.total_jobs}")
    print(f"  Successful        : {summary.successful}")
    print(f"  Failed            : {summary.failed}")

    if summary.failures_by_reason:
        print("  Failures by reason:")
        for reason, count in summary.failures_by_reason.items():
            print(f"    - {reason:<12}: {count}")

    print(f"\n  Wall-clock time   : {summary.wall_clock_seconds:.2f}s  (concurrent)")
    print(f"  Sequential would  : {summary.estimated_sequential_seconds:.2f}s")
    print(f"  [SPEEDUP]         : {summary.speedup}x faster")
    print("=" * 50)


async def main() -> None:
    jobs = create_jobs()

    print(f"Submitting {len(jobs)} jobs to the batch processor...")
    print(f"  max_concurrency = 3   |   timeout_per_job = 3.0 s\n")

    summary = await batch_supervisor(
        jobs,
        max_concurrency=3,
        timeout_seconds=3.0,   # LOW priority jobs (~4 s) will time out
    )

    print_summary(summary)


if __name__ == "__main__":
    asyncio.run(main())
