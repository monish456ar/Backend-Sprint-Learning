from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ── Enums ──────────────────────────────────────────────────────────────────

class JobType(Enum):
    ETL = "etl"
    REPORT = "report"
    SYNC = "sync"
    CLEANUP = "cleanup"


class Priority(Enum):
    """
    Lower number = higher priority = faster simulated processing.
    HIGH  → ~1 s,  MEDIUM → ~2 s,  LOW → ~4 s
    """
    HIGH = 1
    MEDIUM = 2
    LOW = 4


class FailureReason(Enum):
    TIMEOUT = "timeout"
    ERROR = "error"


# ── Core data structures ───────────────────────────────────────────────────

@dataclass
class Job:
    """A single enrichment job dispatched to the batch processor."""
    id: str                          # unique identifier  e.g. "job-001"
    job_type: JobType
    priority: Priority
    payload: Any                     # arbitrary typed payload


@dataclass
class JobResult:
    """Outcome produced after processing one Job."""
    job_id: str
    success: bool
    duration_seconds: float
    failure_reason: FailureReason | None = None  # only set when success=False


@dataclass
class BatchSummary:
    """Aggregate summary produced at the end of a full batch run."""
    total_jobs: int
    successful: int
    failed: int
    # break down failures by reason  → {"timeout": 2, "error": 1}
    failures_by_reason: dict[str, int] = field(default_factory=dict)
    wall_clock_seconds: float = 0.0
    estimated_sequential_seconds: float = 0.0  # sum of individual durations

    @property
    def speedup(self) -> float:
        """How much faster concurrent was vs sequential (approx)."""
        if self.wall_clock_seconds == 0:
            return 0.0
        return round(self.estimated_sequential_seconds / self.wall_clock_seconds, 2)
