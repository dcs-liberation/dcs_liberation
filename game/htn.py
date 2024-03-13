from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar

WorldStateT = TypeVar("WorldStateT", bound="WorldState[Any]")


class WorldState(ABC, Generic[WorldStateT]):
    @abstractmethod
    def clone(self) -> WorldStateT:
        ...


class Task(Generic[WorldStateT]):
    pass


Method = Sequence[Task[WorldStateT]]


class PrimitiveTask(Task[WorldStateT], Generic[WorldStateT], ABC):
    @abstractmethod
    def preconditions_met(self, state: WorldStateT) -> bool:
        ...

    @abstractmethod
    def apply_effects(self, state: WorldStateT) -> None:
        ...


class CompoundTask(Task[WorldStateT], Generic[WorldStateT], ABC):
    @abstractmethod
    def each_valid_method(self, state: WorldStateT) -> Iterator[Method[WorldStateT]]:
        ...


PrimitiveTaskT = TypeVar("PrimitiveTaskT", bound=PrimitiveTask[Any])


@dataclass
class PlanningState(Generic[WorldStateT, PrimitiveTaskT]):
    state: WorldStateT
    tasks_to_process: deque[Task[WorldStateT]]
    plan: list[PrimitiveTaskT]
    methods: Optional[Iterator[Method[WorldStateT]]]


@dataclass(frozen=True)
class PlanningResult(Generic[WorldStateT, PrimitiveTaskT]):
    tasks: list[PrimitiveTaskT]
    end_state: WorldStateT


class PlanningHistory(Generic[WorldStateT, PrimitiveTaskT]):
    def __init__(self) -> None:
        self.states: list[PlanningState[WorldStateT, PrimitiveTaskT]] = []

    def push(self, planning_state: PlanningState[WorldStateT, PrimitiveTaskT]) -> None:
        self.states.append(planning_state)

    def pop(self) -> PlanningState[WorldStateT, PrimitiveTaskT]:
        return self.states.pop()


class Planner(Generic[WorldStateT, PrimitiveTaskT]):
    def __init__(self, main_task: Task[WorldStateT]) -> None:
        self.main_task = main_task

    def plan(
        self, initial_state: WorldStateT
    ) -> Optional[PlanningResult[WorldStateT, PrimitiveTaskT]]:
        planning_state: PlanningState[WorldStateT, PrimitiveTaskT] = PlanningState(
            initial_state, deque([self.main_task]), [], None
        )
        history: PlanningHistory[WorldStateT, PrimitiveTaskT] = PlanningHistory()
        while planning_state.tasks_to_process:
            task = planning_state.tasks_to_process.popleft()
            if isinstance(task, PrimitiveTask):
                if task.preconditions_met(planning_state.state):
                    task.apply_effects(planning_state.state)
                    # Ignore type erasure. We've already verified that this is a Planner
                    # with a WorldStateT and a PrimitiveTaskT, so we know that the task
                    # list is a list of CompoundTask[WorldStateT] and PrimitiveTaskT. We
                    # could scatter more unions throughout to be more explicit but
                    # there's no way around the type erasure that mypy uses for
                    # isinstance.
                    planning_state.plan.append(task)  # type: ignore
                else:
                    planning_state = history.pop()
            else:
                assert isinstance(task, CompoundTask)
                # If the methods field of our current state is not None that means we're
                # resuming a prior attempt to execute this task after a subtask of the
                # previously selected method failed.
                #
                # Otherwise this is the first exectution of this task so we need to
                # create the generator.
                if planning_state.methods is None:
                    methods = task.each_valid_method(planning_state.state)
                else:
                    methods = planning_state.methods
                try:
                    method = next(methods)
                    # Push the current node back onto the stack so that we resume
                    # handling this task when we pop back to this state.
                    resume_tasks: deque[Task[WorldStateT]] = deque([task])
                    resume_tasks.extend(planning_state.tasks_to_process)
                    history.push(
                        PlanningState(
                            planning_state.state.clone(),
                            resume_tasks,
                            planning_state.plan,
                            methods,
                        )
                    )
                    planning_state.methods = None
                    planning_state.tasks_to_process.extendleft(reversed(method))
                except StopIteration:
                    try:
                        planning_state = history.pop()
                    except IndexError:
                        # No valid plan was found.
                        return None
        return PlanningResult(planning_state.plan, planning_state.state)
