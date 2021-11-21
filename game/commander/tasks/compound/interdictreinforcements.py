from collections.abc import Iterator

from game.commander.tasks.primitive.antishipping import PlanAntiShipping
from game.commander.tasks.primitive.convoyinterdiction import PlanConvoyInterdiction
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


class InterdictReinforcements(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        # These will only rarely get planned. When a convoy is travelling multiple legs,
        # they're targetable after the first leg. The reason for this is that
        # procurement happens *after* mission planning so that the missions that could
        # not be filled will guide the procurement process. Procurement is the stage
        # that convoys are created (because they're created to move ground units that
        # were just purchased), so we haven't created any yet. Any incomplete transfers
        # from the previous turn (multi-leg journeys) will still be present though so
        # they can be targeted.
        #
        # Even after this is fixed, the player's convoys that were created through the
        # UI will never be targeted on the first turn of their journey because the AI
        # stops planning after the start of the turn. We could potentially fix this by
        # moving opfor mission planning until the takeoff button is pushed.
        for convoy in state.enemy_convoys:
            yield [PlanConvoyInterdiction(convoy)]
        for ship in state.enemy_shipping:
            yield [PlanAntiShipping(ship)]
