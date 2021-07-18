# Measuring estimated fuel consumption

To estimate fuel consumption numbers for an aircraft, create a mission with a
typical heavy load for the aircraft. For example, to measure for the F/A-18C, a
loadout with two bags, two GBU-31s, two sidewinders, an AMRAAM, and an ATFLIR.
Do **not** drop bags or weapons during the test flight.

Start the aircraft on the ground at a large airport (for example, Akrotiri) at a
parking space at the opposite end of the takeoff runway so you can estimate long
taxi fuel consumption.

When you enter the jet, note the amount of fuel below, then taxi to the far end
of the runway. Hold short and note the remaining fuel below.

Follow a typical takeoff pattern for the aircraft. For the F/A-18C, this might
be AB takeoff, reduce to MIL at 350KIAS, and maintian 350KIAS/0.85 mach until
cruise altitude (angles 25).

Once you reach angels 25, pause the game. Note your remaining fuel below and
measure the distance traveled from takeoff. Mark your location on the map.

Level out and increase to cruise speed if needed. Liberation assumes 0.85 mach
for supersonic aircraft, for subsonic aircraft it depends so pick something
reasonable and note your descision in a comment in the file when done. Maintain
speed, heading, and altitude for a long distance (the longer the distance, the
more accurate the result, but be careful to leave enough fuel for the final
section). Once complete, note the distance traveled and the remaining fuel.

Finally, increase speed as you would for an attack. At least MIL power,
potentially use AB sparingly, etc. The goal is to measure fuel consumption per
mile traveled during an attack run.

```
start:
taxi end:
to 25k distance:
at 25k fuel:
cruise (.85 mach) distance:
cruise (.85 mach) end fuel:
combat distance:
combat end fuel:
```

Finally, fill out the data in the aircraft data. Below is an example for the
F/A-18C:

```
start: 15290
taxi end: 15120
climb distance: 40NM
at 25k fuel: 13350
cruise (.85 mach) distance: 100NM
cruise (.85 mach) end fuel: 11140
combat distance: 100NM
combat end fuel: 8390

taxi = start - taxi end = 15290 - 15120 = 170
climb fuel = taxi end - at 25k fuel = 15120 - 13350 = 1770
climb ppm = climb fuel / climb distance =  1770 / 40 = 44.25
cruise fuel = at 25k fuel - cruise end fuel = 13350 - 11140 = 2210
cruise ppm = cruise fuel / cruise distance = 2210 / 100 = 22.1
combat fuel = cruise end fuel - combat end fuel = 11140 - 8390 = 2750
combat ppm = combat fuel / combat distance = 2750 / 100 = 27.5
```

```yaml
fuel:
  # Parking A1 to RWY 32 at Akrotiri.
  taxi: 170
  # AB takeoff to 350/0.85, reduce to MIL and maintain 350 to 25k ft.
  climb_ppm: 44.25
  # 0.85 mach for 100NM.
  cruise_ppm: 22.1
  # ~0.9 mach for 100NM. Occasional AB use.
  combat_ppm: 27.5
  min_safe: 2000
```

The last entry (`min_safe`) is the minimum amount of fuel that the aircraft
should land with.
