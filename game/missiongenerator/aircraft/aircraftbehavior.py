import logging
from typing import Any, Optional

from dcs.task import (
    AWACS,
    AWACSTaskAction,
    AntishipStrike,
    CAP,
    CAS,
    EPLRS,
    FighterSweep,
    GroundAttack,
    Nothing,
    OptROE,
    OptRTBOnBingoFuel,
    OptRTBOnOutOfAmmo,
    OptReactOnThreat,
    OptRestrictJettison,
    Refueling,
    RunwayAttack,
    Transport,
)
from dcs.unitgroup import FlyingGroup

from game.ato import Flight, FlightType
from game.ato.flightplans.aewc import AewcFlightPlan
from game.ato.flightplans.shiprecoverytanker import RecoveryTankerFlightPlan
from game.ato.flightplans.theaterrefueling import TheaterRefuelingFlightPlan


class AircraftBehavior:
    def __init__(self, task: FlightType) -> None:
        self.task = task

    def apply_to(self, flight: Flight, group: FlyingGroup[Any]) -> None:
        if self.task in [
            FlightType.BARCAP,
            FlightType.TARCAP,
            FlightType.INTERCEPTION,
        ]:
            self.configure_cap(group, flight)
        elif self.task == FlightType.SWEEP:
            self.configure_sweep(group, flight)
        elif self.task == FlightType.AEWC:
            self.configure_awacs(group, flight)
        elif self.task == FlightType.REFUELING:
            self.configure_refueling(group, flight)
        elif self.task in [FlightType.CAS, FlightType.BAI]:
            self.configure_cas(group, flight)
        elif self.task == FlightType.DEAD:
            self.configure_dead(group, flight)
        elif self.task == FlightType.SEAD:
            self.configure_sead(group, flight)
        elif self.task == FlightType.SEAD_ESCORT:
            self.configure_sead_escort(group, flight)
        elif self.task == FlightType.STRIKE:
            self.configure_strike(group, flight)
        elif self.task == FlightType.ANTISHIP:
            self.configure_anti_ship(group, flight)
        elif self.task == FlightType.ESCORT:
            self.configure_escort(group, flight)
        elif self.task == FlightType.OCA_RUNWAY:
            self.configure_runway_attack(group, flight)
        elif self.task == FlightType.OCA_AIRCRAFT:
            self.configure_oca_strike(group, flight)
        elif self.task in [
            FlightType.TRANSPORT,
            FlightType.AIR_ASSAULT,
        ]:
            self.configure_transport(group, flight)
        elif self.task == FlightType.FERRY:
            self.configure_ferry(group, flight)
        else:
            self.configure_unknown_task(group, flight)

        self.configure_eplrs(group, flight)

    def configure_behavior(
        self,
        flight: Flight,
        group: FlyingGroup[Any],
        react_on_threat: OptReactOnThreat.Values = OptReactOnThreat.Values.EvadeFire,
        roe: Optional[int] = None,
        rtb_winchester: Optional[OptRTBOnOutOfAmmo.Values] = None,
        restrict_jettison: Optional[bool] = None,
        mission_uses_gun: bool = True,
    ) -> None:
        group.points[0].tasks.clear()
        group.points[0].tasks.append(OptReactOnThreat(react_on_threat))
        if roe is not None:
            group.points[0].tasks.append(OptROE(roe))
        if restrict_jettison is not None:
            group.points[0].tasks.append(OptRestrictJettison(restrict_jettison))
        if rtb_winchester is not None:
            group.points[0].tasks.append(OptRTBOnOutOfAmmo(rtb_winchester))

        # Confiscate the bullets of AI missions that do not rely on the gun. There is no
        # "all but gun" RTB winchester option, so air to ground missions with mixed
        # weapon types will insist on using all of their bullets after running out of
        # missiles and bombs. Take away their bullets so they don't strafe a Tor.
        #
        # Exceptions are made for player flights and for airframes where the gun is
        # essential like the A-10 or warbirds.
        if not mission_uses_gun and not self.flight_always_keeps_gun(flight):
            for unit in group.units:
                unit.gun = 0

        group.points[0].tasks.append(OptRTBOnBingoFuel(True))
        # Do not restrict afterburner.
        # https://forums.eagle.ru/forum/english/digital-combat-simulator/dcs-world-2-5/bugs-and-problems-ai/ai-ad/7121294-ai-stuck-at-high-aoa-after-making-sharp-turn-if-afterburner-is-restricted

    @staticmethod
    def configure_eplrs(group: FlyingGroup[Any], flight: Flight) -> None:
        if flight.unit_type.eplrs_capable:
            group.points[0].tasks.append(EPLRS(group.id))

    def configure_cap(self, group: FlyingGroup[Any], flight: Flight) -> None:
        group.task = CAP.name

        if not flight.unit_type.gunfighter:
            ammo_type = OptRTBOnOutOfAmmo.Values.AAM
        else:
            ammo_type = OptRTBOnOutOfAmmo.Values.Cannon

        self.configure_behavior(flight, group, rtb_winchester=ammo_type)

    def configure_sweep(self, group: FlyingGroup[Any], flight: Flight) -> None:
        group.task = FighterSweep.name

        if not flight.unit_type.gunfighter:
            ammo_type = OptRTBOnOutOfAmmo.Values.AAM
        else:
            ammo_type = OptRTBOnOutOfAmmo.Values.Cannon

        self.configure_behavior(flight, group, rtb_winchester=ammo_type)

    def configure_cas(self, group: FlyingGroup[Any], flight: Flight) -> None:
        group.task = CAS.name
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            rtb_winchester=OptRTBOnOutOfAmmo.Values.Unguided,
            restrict_jettison=True,
        )

    def configure_dead(self, group: FlyingGroup[Any], flight: Flight) -> None:
        # Only CAS and SEAD are capable of the Attack Group task. SEAD is arguably more
        # appropriate but it has an extremely limited list of capable aircraft, whereas
        # CAS has a much wider selection of units.
        #
        # Note that the only effect that the DCS task type has is in determining which
        # waypoint actions the group may perform.
        group.task = CAS.name
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            rtb_winchester=OptRTBOnOutOfAmmo.Values.All,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_sead(self, group: FlyingGroup[Any], flight: Flight) -> None:
        # CAS is able to perform all the same tasks as SEAD using a superset of the
        # available aircraft, and F-14s are not able to be SEAD despite having TALDs.
        # https://forums.eagle.ru/topic/272112-cannot-assign-f-14-to-sead/
        group.task = CAS.name
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            # ASM includes ARMs and TALDs (among other things, but those are the useful
            # weapons for SEAD).
            rtb_winchester=OptRTBOnOutOfAmmo.Values.ASM,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_strike(self, group: FlyingGroup[Any], flight: Flight) -> None:
        group.task = GroundAttack.name
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_anti_ship(self, group: FlyingGroup[Any], flight: Flight) -> None:
        group.task = AntishipStrike.name
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_runway_attack(self, group: FlyingGroup[Any], flight: Flight) -> None:
        group.task = RunwayAttack.name
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_oca_strike(self, group: FlyingGroup[Any], flight: Flight) -> None:
        group.task = CAS.name
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
        )

    def configure_awacs(self, group: FlyingGroup[Any], flight: Flight) -> None:
        group.task = AWACS.name

        if not isinstance(flight.flight_plan, AewcFlightPlan):
            logging.error(
                f"Cannot configure AEW&C tasks for {flight} because it does not have "
                "an AEW&C flight plan."
            )
            return

        # Awacs task action
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.WeaponHold,
            restrict_jettison=True,
        )

        group.points[0].tasks.append(AWACSTaskAction())

    def configure_refueling(self, group: FlyingGroup[Any], flight: Flight) -> None:
        group.task = Refueling.name

        if not (
            isinstance(flight.flight_plan, TheaterRefuelingFlightPlan)
            or isinstance(flight.flight_plan, RecoveryTankerFlightPlan)
        ):
            logging.error(
                f"Cannot configure racetrack refueling tasks for {flight} because it "
                "does not have an racetrack refueling flight plan."
            )
            return

        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.WeaponHold,
            restrict_jettison=True,
        )

    def configure_escort(self, group: FlyingGroup[Any], flight: Flight) -> None:
        # Escort groups are actually given the CAP task so they can perform the
        # Search Then Engage task, which we have to use instead of the Escort
        # task for the reasons explained in JoinPointBuilder.
        group.task = CAP.name
        self.configure_behavior(
            flight, group, roe=OptROE.Values.OpenFire, restrict_jettison=True
        )

    def configure_sead_escort(self, group: FlyingGroup[Any], flight: Flight) -> None:
        # CAS is able to perform all the same tasks as SEAD using a superset of the
        # available aircraft, and F-14s are not able to be SEAD despite having TALDs.
        # https://forums.eagle.ru/topic/272112-cannot-assign-f-14-to-sead/
        group.task = CAS.name
        self.configure_behavior(
            flight,
            group,
            roe=OptROE.Values.OpenFire,
            # ASM includes ARMs and TALDs (among other things, but those are the useful
            # weapons for SEAD).
            rtb_winchester=OptRTBOnOutOfAmmo.Values.ASM,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_transport(self, group: FlyingGroup[Any], flight: Flight) -> None:
        group.task = Transport.name
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.WeaponHold,
            restrict_jettison=True,
        )

    def configure_ferry(self, group: FlyingGroup[Any], flight: Flight) -> None:
        group.task = Nothing.name
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.WeaponHold,
            restrict_jettison=True,
        )

    def configure_unknown_task(self, group: FlyingGroup[Any], flight: Flight) -> None:
        logging.error(f"Unhandled flight type: {flight.flight_type}")
        self.configure_behavior(flight, group)

    @staticmethod
    def flight_always_keeps_gun(flight: Flight) -> bool:
        # Never take bullets from players. They're smart enough to know when to use it
        # and when to RTB.
        if flight.client_count > 0:
            return True

        return flight.unit_type.always_keeps_gun
