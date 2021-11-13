"""The Theater Commander is the highest level campaign AI.

Target selection is performed with a hierarchical-task-network (HTN, linked below).
These work by giving the planner an initial "task" which decomposes into other tasks
until a concrete set of actions is formed. For example, the "capture base" task may
decompose in the following manner:

* Defend
  * Reinforce front line
  * Set front line stance to defend
  * Destroy enemy front line units
      * Set front line stance to elimination
      * Plan CAS at front line
* Prepare
  * Destroy enemy IADS
    * Plan DEAD against SAM Armadillo
    * ...
  * Destroy enemy front line units
      * Set front line stance to elimination
      * Plan CAS at front line
* Inhibit
  * Destroy enemy unit production infrastructure
    * Destroy factory at Palmyra
    * ...
  * Destroy enemy front line units
      * Set front line stance to elimination
      * Plan CAS at front line
* Attack
  * Set front line stance to breakthrough
  * Destroy enemy front line units
      * Set front line stance to elimination
      * Plan CAS at front line

This is not a reflection of the actual task composition but illustrates the capability
of the system. Each task has preconditions which are checked before the task is
decomposed. If preconditions are not met the task is ignored and the next is considered.
For example the task to destroy the factory at Palmyra might be excluded until the air
defenses protecting it are eliminated; or defensive air operations might be excluded if
the enemy does not have sufficient air forces, or if the protected target has sufficient
SAM coverage.

Each action updates the world state, which causes each action to account for the result
of the tasks executed before it. Above, the preconditions for attacking the factory at
Palmyra may not have been met due to the IADS coverage, leading the planning to decide
on an attack against the IADS in the area instead. When planning the next task in the
same turn, the world state will have been updated to account for the (hopefully)
destroyed SAM sites, allowing the planner to choose the mission to attack the factory.

Preconditions can be aware of previous actions as well. A precondition for "Plan CAS at
front line" can be "No CAS missions planned at front line" to avoid over-planning CAS
even though it is a primitive task used by many other tasks.

https://en.wikipedia.org/wiki/Hierarchical_task_network
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from game.ato.starttype import StartType
from game.commander.tasks.compound.nextaction import PlanNextAction
from game.commander.tasks.theatercommandertask import TheaterCommanderTask
from game.commander.theaterstate import TheaterState
from game.htn import Planner
from game.profiling import MultiEventTracer

if TYPE_CHECKING:
    from game import Game


class TheaterCommander(Planner[TheaterState, TheaterCommanderTask]):
    def __init__(self, game: Game, player: bool) -> None:
        super().__init__(
            PlanNextAction(
                aircraft_cold_start=game.settings.default_start_type is StartType.COLD
            )
        )
        self.game = game
        self.player = player

    def plan_missions(self, tracer: MultiEventTracer) -> None:
        state = TheaterState.from_game(self.game, self.player, tracer)
        while True:
            result = self.plan(state)
            if result is None:
                # Planned all viable tasks this turn.
                return
            for task in result.tasks:
                task.execute(self.game.coalition_for(self.player))
            state = result.end_state
