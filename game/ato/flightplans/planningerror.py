from __future__ import annotations


class PlanningError(RuntimeError):
    """Raised when the flight planner was unable to create a flight plan."""
