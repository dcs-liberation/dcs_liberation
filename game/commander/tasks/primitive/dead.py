from __future__ import annotations

from dataclasses import dataclass

from game.commander.missionproposals import EscortType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater.theatergroundobject import IadsGroundObject
from game.ato.flighttype import FlightType


@dataclass
class PlanDead(PackagePlanningTask[IadsGroundObject]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if (
            self.target not in state.threatening_air_defenses
            and self.target not in state.detecting_air_defenses
        ):
            return False
        if not self.target_area_preconditions_met(state, ignore_iads=True):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.eliminate_air_defense(self.target)

    def propose_flights(self) -> None:
        self.propose_flight(FlightType.DEAD, 2)

        # Only include SEAD against SAMs that still have emitters. No need to
        # suppress an EWR, and SEAD isn't useful against a SAM that no longer has a
        # working track radar.
        #
        # For SAMs without track radars and EWRs, we still want a SEAD escort if
        # needed.
        #
        # Note that there is a quirk here: we should potentially be included a SEAD
        # escort *and* SEAD when the target is a radar SAM but the flight path is
        # also threatened by SAMs. We don't want to include a SEAD escort if the
        # package is *only* threatened by the target though. Could be improved, but
        # needs a decent refactor to the escort planning to do so.
        if self.target.has_live_radar_sam:
            self.propose_flight(FlightType.SEAD, 2)
        else:
            self.propose_flight(FlightType.SEAD_ESCORT, 2, EscortType.Sead)
        self.propose_flight(FlightType.ESCORT, 2, EscortType.AirToAir)
