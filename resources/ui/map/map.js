// Won't actually enable anything unless the same property is set in
// mapmodel.py.
const ENABLE_EXPENSIVE_DEBUG_TOOLS = false;

const Colors = Object.freeze({
  Blue: "#0084ff",
  Red: "#c85050",
  Green: "#80BA80",
  Highlight: "#ffff00",
});

const Categories = Object.freeze([
  "aa",
  "allycamp",
  "ammo",
  "armor",
  "coastal",
  "comms",
  "derrick",
  "ewr",
  "factory",
  "farp",
  "fuel",
  "missile",
  "oil",
  "power",
  "ship",
  "village",
  "ware",
  "ww2bunker",
]);

const UnitState = Object.freeze({
  Alive: "alive",
  Damaged: "damaged",
  Destroyed: "destroyed",
});

class CpIcons {
  constructor() {
    this.icons = {};
    for (const player of [true, false]) {
      this.icons[player] = {};
      for (const state of Object.values(UnitState)) {
        this.icons[player][state] = {
          airfield: this.loadIcon("airfield", player, state),
          cv: this.loadIcon("cv", player, state),
          fob: this.loadIcon("fob", player, state),
          lha: this.loadIcon("lha", player, state),
          offmap: this.loadIcon("airfield", player, state),
        };
      }
    }
  }

  icon(category, player, state) {
    return this.icons[player][state][category];
  }

  loadIcon(category, player, state) {
    const color = player ? "blue" : "red";
    return new L.Icon({
      iconUrl: `../ground_assets/${category}_${color}_${state}.svg`,
      iconSize: [32, 32],
    });
  }
}

class TgoIcons {
  constructor() {
    this.icons = {};
    for (const category of Categories) {
      this.icons[category] = {};
      for (const player of [true, false]) {
        this.icons[category][player] = {};
        for (const state of Object.values(UnitState)) {
          this.icons[category][player][state] = this.loadIcon(
            category,
            player,
            state
          );
        }
      }
    }
  }

  icon(category, player, state) {
    return this.icons[category][player][state];
  }

  loadIcon(category, player, state) {
    const color = player ? "blue" : "red";
    return new L.Icon({
      iconUrl: `../ground_assets/${category}_${color}_${state}.svg`,
      iconSize: [32, 32],
    });
  }

  loadLegacyIcon(category, player) {
    const playerSuffix = player ? "_blue" : "";
    return new L.Icon({
      iconUrl: `../ground_assets/${category}${playerSuffix}.png`,
    });
  }
}

class AirIcons {
  constructor() {
    this.icons = {};
    for (const player of [true, false]) {
      this.icons[player] = {};
      for (const selected of [true, false]) {
        this.icons[player][selected] = this.loadIcon(
          "unspecified",
          player,
          selected
        );
      }
    }
  }

  icon(_category, player, selected) {
    return this.icons[player][selected];
  }

  loadIcon(category, player, selected) {
    var color;
    if (selected) {
      color = "selected";
    } else {
      color = player ? "blue" : "red";
    }
    return new L.Icon({
      iconUrl: `../air_assets/${category}_${color}.svg`,
      iconSize: [24, 24],
    });
  }
}

const Icons = Object.freeze({
  ControlPoints: new CpIcons(),
  Objectives: new TgoIcons(),
  AirIcons: new AirIcons(),
});

function metersToNauticalMiles(meters) {
  return meters * 0.000539957;
}

function formatLatLng(latLng) {
  const lat = latLng.lat.toFixed(2);
  const lng = latLng.lng.toFixed(2);
  const ns = lat >= 0 ? "N" : "S";
  const ew = lng >= 0 ? "E" : "W";
  return `${lat}&deg;${ns} ${lng}&deg;${ew}`;
}

const map = L.map("map", {
  doubleClickZoom: false,
  zoomControl: false,
}).setView([0, 0], 3);
L.control.scale({ maxWidth: 200 }).addTo(map);

const rulerOptions = {
  position: "topleft",
  circleMarker: {
    color: Colors.Highlight,
    radius: 2,
  },
  lineStyle: {
    color: Colors.Highlight,
    dashArray: "1,6",
  },
  lengthUnit: {
    display: "nm",
    decimal: "2",
    factor: 0.539956803,
    label: "Distance:",
  },
  angleUnit: {
    display: "&deg;",
    decimal: 0,
    label: "Bearing:",
  },
};
L.control.ruler(rulerOptions).addTo(map);

// https://esri.github.io/esri-leaflet/api-reference/layers/basemap-layer.html
const baseLayers = {
  "Imagery Clarity": L.esri.basemapLayer("ImageryClarity", { maxZoom: 17 }),
  "Imagery Firefly": L.esri.basemapLayer("ImageryFirefly", { maxZoom: 17 }),
  Topographic: L.esri.basemapLayer("Topographic", { maxZoom: 16 }),
};

const defaultBaseMap = baseLayers["Imagery Clarity"];
defaultBaseMap.addTo(map);

// Enabled by default, so addTo(map).
const controlPointsLayer = L.layerGroup().addTo(map);
const aircraftLayer = L.layerGroup().addTo(map);
const airDefensesLayer = L.layerGroup().addTo(map);
const factoriesLayer = L.layerGroup().addTo(map);
const shipsLayer = L.layerGroup().addTo(map);
const groundObjectsLayer = L.layerGroup().addTo(map);
const supplyRoutesLayer = L.layerGroup().addTo(map);
const frontLinesLayer = L.layerGroup().addTo(map);
const redSamThreatLayer = L.layerGroup().addTo(map);
const blueFlightPlansLayer = L.layerGroup().addTo(map);
const combatLayer = L.layerGroup().addTo(map);

// Added to map by the user via layer controls.
const blueSamThreatLayer = L.layerGroup();
const blueSamDetectionLayer = L.layerGroup();
const redSamDetectionLayer = L.layerGroup();
const redFlightPlansLayer = L.layerGroup();
const selectedFlightPlansLayer = L.layerGroup();
const allFlightPlansLayer = L.layerGroup();

const blueFullThreatZones = L.layerGroup();
const blueAircraftThreatZones = L.layerGroup();
const blueAirDefenseThreatZones = L.layerGroup();
const blueRadarSamThreatZones = L.layerGroup();

const redFullThreatZones = L.layerGroup();
const redAircraftThreatZones = L.layerGroup();
const redAirDefenseThreatZones = L.layerGroup();
const redRadarSamThreatZones = L.layerGroup();

const blueNavmesh = L.layerGroup();
const redNavmesh = L.layerGroup();

const inclusionZones = L.layerGroup();
const exclusionZones = L.layerGroup();
const seaZones = L.layerGroup();
const unculledZones = L.layerGroup();

const noWaypointZones = L.layerGroup();
const ipZones = L.layerGroup();
const joinZones = L.layerGroup();
const holdZones = L.layerGroup();

const debugControlGroups = {
  "Blue Threat Zones": {
    Hide: L.layerGroup().addTo(map),
    Full: blueFullThreatZones,
    Aircraft: blueAircraftThreatZones,
    "Air Defenses": blueAirDefenseThreatZones,
    "Radar SAMs": blueRadarSamThreatZones,
  },
  "Red Threat Zones": {
    Hide: L.layerGroup().addTo(map),
    Full: redFullThreatZones,
    Aircraft: redAircraftThreatZones,
    "Air Defenses": redAirDefenseThreatZones,
    "Radar SAMs": redRadarSamThreatZones,
  },
  Navmeshes: {
    Hide: L.layerGroup().addTo(map),
    Blue: blueNavmesh,
    Red: redNavmesh,
  },
  "Map Zones": {
    "Inclusion zones": inclusionZones,
    "Exclusion zones": exclusionZones,
    "Sea zones": seaZones,
    "Culling exclusion zones": unculledZones,
  },
};

if (ENABLE_EXPENSIVE_DEBUG_TOOLS) {
  debugControlGroups["Waypoint Zones"] = {
    None: noWaypointZones,
    "IP Zones": ipZones,
    "Join Zones": joinZones,
    "Hold Zones": holdZones,
  };
}

// Main map controls. These are the ones that we expect users to interact with.
// These are always open, which unfortunately means that the scroll bar will not
// appear if the menu doesn't fit. This fits in the smallest window size we
// allow, but may need to start auto-collapsing it (or fix the plugin to add a
// scrollbar when non-collapsing) if it gets much larger.
L.control
  .groupedLayers(
    baseLayers,
    {
      "Units and locations": {
        "Control points": controlPointsLayer,
        Aircraft: aircraftLayer,
        "Active combat": combatLayer,
        "Air defenses": airDefensesLayer,
        Factories: factoriesLayer,
        Ships: shipsLayer,
        "Other ground objects": groundObjectsLayer,
        "Supply routes": supplyRoutesLayer,
        "Front lines": frontLinesLayer,
      },
      "Enemy Air Defenses": {
        "Enemy SAM threat range": redSamThreatLayer,
        "Enemy SAM detection range": redSamDetectionLayer,
      },
      "Allied Air Defenses": {
        "Ally SAM threat range": blueSamThreatLayer,
        "Ally SAM detection range": blueSamDetectionLayer,
      },
      "Flight Plans": {
        Hide: L.layerGroup(),
        "Show selected blue": selectedFlightPlansLayer,
        "Show all blue": blueFlightPlansLayer,
        "Show all red": redFlightPlansLayer,
        "Show all": allFlightPlansLayer,
      },
    },
    {
      collapsed: false,
      exclusiveGroups: ["Flight Plans"],
      groupCheckboxes: true,
    }
  )
  .addTo(map);

// Debug map controls. Hover over to open. Not something most users will want or
// need to interact with.
L.control
  .groupedLayers(null, debugControlGroups, {
    position: "topleft",
    exclusiveGroups: [
      "Blue Threat Zones",
      "Red Threat Zones",
      "Navmeshes",
      "Waypoint Zones",
    ],
    groupCheckboxes: true,
  })
  .addTo(map);

let game;
new QWebChannel(qt.webChannelTransport, function (channel) {
  game = channel.objects.game;
  drawInitialMap();
  game.cleared.connect(clearAllLayers);
  game.mapCenterChanged.connect(recenterMap);
  game.controlPointsChanged.connect(drawControlPoints);
  game.groundObjectsChanged.connect(drawGroundObjects);
  game.supplyRoutesChanged.connect(drawSupplyRoutes);
  game.frontLinesChanged.connect(drawFrontLines);
  game.flightsChanged.connect(drawAircraft);
  game.threatZonesChanged.connect(drawThreatZones);
  game.navmeshesChanged.connect(drawNavmeshes);
  game.mapZonesChanged.connect(drawMapZones);
  game.unculledZonesChanged.connect(drawUnculledZones);
  game.ipZonesChanged.connect(drawIpZones);
  game.joinZonesChanged.connect(drawJoinZones);
  game.holdZonesChanged.connect(drawHoldZones);
  game.airCombatsChanged.connect(drawCombat);
  game.samCombatsChanged.connect(drawCombat);
  game.ipCombatsChanged.connect(drawCombat);
});

function recenterMap(center) {
  map.setView(center, 8, { animate: true, duration: 1 });
}

class ControlPoint {
  constructor(cp) {
    this.cp = cp;
    // The behavior we want is for the CP to be draggable when it has no
    // destination, but for the destination to be draggable when it does. The
    // primary marker is always shown and draggable. When a destination exists,
    // the primary marker marks the destination and the secondary marker marks
    // the location. When no destination exists, the primary marker marks the
    // location and the secondary marker is not shown.
    this.primaryMarker = this.makePrimaryMarker();
    this.secondaryMarker = this.makeSecondaryMarker();
    this.path = this.makePath();
    this.attachTooltipsAndHandlers();
    this.cp.destinationChanged.connect(() => this.onDestinationChanged());
  }

  icon() {
    return Icons.ControlPoints.icon(
      this.cp.category,
      this.cp.blue,
      this.cp.status
    );
  }

  hasDestination() {
    return this.cp.destination.length > 0;
  }

  hideDestination() {
    this.secondaryMarker.removeFrom(controlPointsLayer);
    this.path.removeFrom(controlPointsLayer);
  }

  setDestination(destination) {
    this.cp.setDestination([destination.lat, destination.lng]).then((err) => {
      if (err) {
        console.log(`Could not set control point destination: ${err}`);
        this.locationMarker().bindPopup(err).openPopup();
        // Reset markers and paths on error. On success this happens when we get
        // the destinationChanged signal from the backend.
        this.onDestinationChanged();
      }
    });
  }

  onDrag(destination) {
    this.path.setLatLngs([this.cp.position, destination]);
    this.path.addTo(controlPointsLayer);
    const distance = metersToNauticalMiles(
      destination.distanceTo(this.cp.position)
    );
    this.primaryMarker.unbindTooltip();
    this.primaryMarker.bindTooltip(
      `Move ${distance.toFixed(1)}nm to ${formatLatLng(destination)}`,
      {
        permanent: true,
      }
    );
    this.cp
      .destinationInRange([destination.lat, destination.lng])
      .then((inRange) => {
        this.path.setStyle({
          color: inRange ? Colors.Green : Colors.Red,
        });
      });
  }

  detachTooltipsAndHandlers() {
    this.primaryMarker.unbindTooltip();
    this.primaryMarker.off("click");
    this.primaryMarker.off("contextmenu");
    this.secondaryMarker.unbindTooltip();
    this.secondaryMarker.off("click");
    this.secondaryMarker.off("contextmenu");
  }

  locationMarker(dragging = false) {
    return this.hasDestination() || dragging
      ? this.secondaryMarker
      : this.primaryMarker;
  }

  destinationMarker() {
    return this.hasDestination() ? this.primaryMarker : null;
  }

  attachTooltipsAndHandlers(dragging = false) {
    this.detachTooltipsAndHandlers();
    const locationMarker = this.locationMarker(dragging);
    const destinationMarker = this.destinationMarker();
    locationMarker
      .bindTooltip(`<h3 style="margin: 0;">${this.cp.name}</h3>`)
      .on("click", () => {
        this.cp.showInfoDialog();
      })
      .on("contextmenu", () => {
        this.cp.showPackageDialog();
      });
    if (destinationMarker != null) {
      const origin = locationMarker.getLatLng();
      const destination = destinationMarker.getLatLng();
      const distance = metersToNauticalMiles(
        destination.distanceTo(origin)
      ).toFixed(1);
      const dest = formatLatLng(destination);
      destinationMarker.bindTooltip(
        `${this.cp.name} moving ${distance}nm to ${dest} next turn`
      );
      destinationMarker.on("contextmenu", () => this.cp.cancelTravel());
      destinationMarker.addTo(map);
    }
  }

  makePrimaryMarker() {
    const location = this.hasDestination()
      ? this.cp.destination
      : this.cp.position;
    // We might draw other markers on top of the CP. The tooltips from the other
    // markers are helpful so we want to keep them, but make sure the CP is
    // always the clickable thing.
    return L.marker(location, {
      icon: this.icon(),
      zIndexOffset: 1000,
      draggable: this.cp.mobile,
      autoPan: true,
    })
      .on("dragstart", () => {
        this.secondaryMarker.addTo(controlPointsLayer);
        this.attachTooltipsAndHandlers(true);
      })
      .on("drag", (event) => {
        const marker = event.target;
        const newPosition = marker.getLatLng();
        this.onDrag(newPosition);
      })
      .on("dragend", (event) => {
        const marker = event.target;
        const newPosition = marker.getLatLng();
        this.setDestination(newPosition);
      })
      .addTo(map);
  }

  makeSecondaryMarker() {
    return L.marker(this.cp.position, {
      icon: this.icon(),
      zIndexOffset: 1000,
    });
  }

  makePath() {
    const destination = this.hasDestination() ? this.cp.destination : [0, 0];
    return L.polyline([this.cp.position, destination], {
      color: Colors.Green,
      weight: 1,
      interactive: false,
    });
  }

  onDestinationChanged() {
    if (this.hasDestination()) {
      this.primaryMarker.setLatLng(this.cp.destination);
      this.primaryMarker.setOpacity(0.5);
      this.secondaryMarker.addTo(controlPointsLayer);
      this.path.setLatLngs([this.cp.position, this.cp.destination]);
      this.path.addTo(controlPointsLayer);
      this.path.setStyle({ color: Colors.Green });
    } else {
      this.hideDestination();
      this.primaryMarker.setLatLng(this.cp.position);
      this.primaryMarker.setOpacity(1);
    }
    this.attachTooltipsAndHandlers();
  }

  drawDestination() {
    this.secondaryMarker.addTo(controlPointsLayer);
    this.path.addTo(controlPointsLayer);
  }

  draw() {
    this.primaryMarker.addTo(controlPointsLayer);
    if (this.hasDestination()) {
      this.drawDestination();
    }
  }
}

function drawControlPoints() {
  controlPointsLayer.clearLayers();
  game.controlPoints.forEach((cp) => {
    new ControlPoint(cp).draw();
  });
}

class TheaterGroundObject {
  constructor(tgo) {
    this.tgo = tgo;
  }

  samIsThreat() {
    for (const range of this.tgo.samThreatRanges) {
      if (range > 0) {
        return true;
      }
    }

    return false;
  }

  icon() {
    let state;
    if (this.tgo.dead) {
      state = UnitState.Destroyed;
    } else if (this.tgo.category == "aa" && !this.samIsThreat()) {
      state = UnitState.Damaged;
    } else {
      state = UnitState.Alive;
    }
    return Icons.Objectives.icon(this.tgo.category, this.tgo.blue, state);
  }

  layer() {
    switch (this.tgo.category) {
      case "aa":
        return airDefensesLayer;
      case "factory":
        return factoriesLayer;
      case "ship":
        return shipsLayer;
      default:
        return groundObjectsLayer;
    }
  }

  drawSamThreats() {
    const detectionLayer = this.tgo.blue
      ? blueSamDetectionLayer
      : redSamDetectionLayer;
    const threatLayer = this.tgo.blue ? blueSamThreatLayer : redSamThreatLayer;
    const threatColor = this.tgo.blue ? Colors.Blue : Colors.Red;
    const detectionColor = this.tgo.blue ? "#bb89ff" : "#eee17b";

    this.tgo.samDetectionRanges.forEach((range) => {
      L.circle(this.tgo.position, {
        radius: range,
        color: detectionColor,
        fill: false,
        weight: 1,
        interactive: false,
      }).addTo(detectionLayer);
    });

    this.tgo.samThreatRanges.forEach((range) => {
      L.circle(this.tgo.position, {
        radius: range,
        color: threatColor,
        fill: false,
        weight: 2,
        interactive: false,
      }).addTo(threatLayer);
    });
  }

  draw() {
    if (!this.tgo.blue && this.tgo.dead) {
      // Don't bother drawing dead opfor TGOs. Blue is worth showing because
      // some of them can be repaired, but the player can't interact with dead
      // red things so there's no point in showing them.
      return;
    }

    L.marker(this.tgo.position, { icon: this.icon() })
      .bindTooltip(
        `${this.tgo.name} (${
          this.tgo.controlPointName
        })<br />${this.tgo.units.join("<br />")}`
      )
      .on("click", () => this.tgo.showInfoDialog())
      .on("contextmenu", () => this.tgo.showPackageDialog())
      .addTo(this.layer());
    this.drawSamThreats();
  }
}

function drawGroundObjects() {
  airDefensesLayer.clearLayers();
  factoriesLayer.clearLayers();
  shipsLayer.clearLayers();
  groundObjectsLayer.clearLayers();
  blueSamDetectionLayer.clearLayers();
  redSamDetectionLayer.clearLayers();
  blueSamThreatLayer.clearLayers();
  redSamThreatLayer.clearLayers();
  game.groundObjects.forEach((tgo) => {
    new TheaterGroundObject(tgo).draw();
  });
}

function drawSupplyRoutes() {
  supplyRoutesLayer.clearLayers();
  game.supplyRoutes.forEach((route) => {
    let color;
    if (route.frontActive) {
      color = Colors.Red;
    } else if (route.blue) {
      color = "#2d3e50";
    } else {
      color = "#8c1414";
    }
    const line = L.polyline(route.points, {
      color: color,
      weight: route.isSea ? 4 : 6,
    }).addTo(supplyRoutesLayer);
    const activeTransports = route.activeTransports;
    if (activeTransports.length > 0) {
      line.bindTooltip(activeTransports.join("<br />"));
      L.polyline(route.points, {
        color: "#ffffff",
        weight: 2,
      }).addTo(supplyRoutesLayer);
    } else {
      line.bindTooltip("This supply route is inactive.");
    }
  });
}

function drawFrontLines() {
  frontLinesLayer.clearLayers();
  game.frontLines.forEach((front) => {
    L.polyline(front.extents, { weight: 8, color: "#fe7d0a" })
      .on("contextmenu", function () {
        front.showPackageDialog();
      })
      .addTo(frontLinesLayer);
  });
}

const SHOW_WAYPOINT_INFO_AT_ZOOM = 9;

class Waypoint {
  constructor(waypoint, flight) {
    this.waypoint = waypoint;
    this.flight = flight;
    this.marker = this.makeMarker();
    this.waypoint.positionChanged.connect(() => this.relocate());
    this.waypoint.timingChanged.connect(() => this.updateDescription());
  }

  position() {
    return this.waypoint.position;
  }

  shouldMark() {
    // We don't need a marker for the departure waypoint (and it's likely
    // coincident with the landing waypoint, so hard to see). We do want to draw
    // the path from it though.
    //
    // We also don't need the landing waypoint since we'll be drawing that path
    // as well and it's clear what it is, and only obscured the CP icon.
    //
    // The divert waypoint also obscures the CP. We don't draw the path to it,
    // but it can be seen in the flight settings page so it's not really a
    // problem to exclude it.
    //
    // Bullseye ought to be (but currently isn't) drawn *once* rather than as a
    // flight waypoint.
    return !(
      this.waypoint.isTakeoff ||
      this.waypoint.isLanding ||
      this.waypoint.isDivert ||
      this.waypoint.isBullseye
    );
  }

  draggable() {
    // Target *points* are the exact location of a unit, whereas the target area
    // is only the center of the objective. Allow moving the latter since its
    // exact location isn't very important.
    //
    // Landing, and divert should be changed in the flight settings UI, takeoff
    // cannot be changed because that's where the plane is.
    //
    // Moving the bullseye reference only makes it wrong.
    return !(
      this.waypoint.isTargetPoint ||
      this.waypoint.isTakeoff ||
      this.waypoint.isLanding ||
      this.waypoint.isDivert ||
      this.waypoint.isBullseye
    );
  }

  description(dragging) {
    const timing = dragging
      ? "Waiting to recompute TOT..."
      : this.waypoint.timing;
    return (
      `${this.waypoint.number} ${this.waypoint.name}<br />` +
      `${this.waypoint.altitudeFt} ft ${this.waypoint.altitudeReference}<br />` +
      `${timing}`
    );
  }

  relocate() {
    this.marker.setLatLng(this.waypoint.position);
  }

  updateDescription(dragging) {
    this.marker.setTooltipContent(this.description(dragging));
  }

  makeMarker() {
    const zoom = map.getZoom();
    return L.marker(this.waypoint.position, { draggable: this.draggable() })
      .bindTooltip(this.description(), {
        permanent: zoom >= SHOW_WAYPOINT_INFO_AT_ZOOM,
      })
      .on("dragstart", (e) => {
        this.updateDescription(true);
      })
      .on("drag", (e) => {
        const marker = e.target;
        const destination = marker.getLatLng();
        this.flight.updatePath(this.waypoint.number, destination);
      })
      .on("dragend", (e) => {
        const marker = e.target;
        const destination = marker.getLatLng();
        this.waypoint
          .setPosition([destination.lat, destination.lng])
          .then((err) => {
            if (err) {
              console.log(err);
              marker.bindPopup(err);
            }
          });
      });
  }

  includeInPath() {
    return !this.waypoint.isDivert && !this.waypoint.isBullseye;
  }
}

class Flight {
  constructor(flight) {
    this.flight = flight;
    this.flightPlan = this.flight.flightPlan.map((p) => new Waypoint(p, this));
    this.aircraft = null;
    this.path = null;
    this.markers = [];
    this.commitBoundary = null;
    this.flight.selectedChanged.connect(() => this.draw());
    this.flight.positionChanged.connect(() => this.drawAircraftLocation());
    this.flight.flightPlanChanged.connect(() => this.drawFlightPlan());
    this.flight.commitBoundaryChanged.connect(() => this.drawCommitBoundary());
  }

  shouldMark(waypoint) {
    return this.flight.selected && waypoint.shouldMark();
  }

  flightPlanLayer() {
    return this.flight.blue ? blueFlightPlansLayer : redFlightPlansLayer;
  }

  updatePath(idx, position) {
    const points = this.path.getLatLngs();
    points[idx] = position;
    this.path.setLatLngs(points);
  }

  drawPath(path) {
    const color = this.flight.blue ? Colors.Blue : Colors.Red;
    const layer = this.flightPlanLayer();
    if (this.flight.selected) {
      this.path = L.polyline(path, {
        color: Colors.Highlight,
        interactive: false,
      })
        .addTo(selectedFlightPlansLayer)
        .addTo(layer)
        .addTo(allFlightPlansLayer);
    } else {
      this.path = L.polyline(path, { color: color, interactive: false })
        .addTo(layer)
        .addTo(allFlightPlansLayer);
    }
  }

  draw() {
    this.drawAircraftLocation();
    this.drawFlightPlan();
    this.drawCommitBoundary();
  }

  drawAircraftLocation() {
    if (this.aircraft != null) {
      this.aircraft.removeFrom(aircraftLayer);
      this.aircraft = null;
    }
    const position = this.flight.position;
    if (position.length > 0) {
      this.aircraft = L.marker(position, {
        icon: Icons.AirIcons.icon(
          "fighter",
          this.flight.blue,
          this.flight.selected
        ),
      }).addTo(aircraftLayer);
    }
  }

  drawCommitBoundary() {
    if (this.commitBoundary != null) {
      this.commitBoundary
        .removeFrom(selectedFlightPlansLayer)
        .removeFrom(this.flightPlanLayer())
        .removeFrom(allFlightPlansLayer);
    }
    if (this.flight.selected) {
      if (this.flight.commitBoundary) {
        this.commitBoundary = L.polyline(this.flight.commitBoundary, {
          color: Colors.Highlight,
          weight: 1,
          interactive: false,
        })
          .addTo(selectedFlightPlansLayer)
          .addTo(this.flightPlanLayer())
          .addTo(allFlightPlansLayer);
      }
    }
  }

  clearFlightPlan() {
    for (const marker of this.markers) {
      marker
        .removeFrom(selectedFlightPlansLayer)
        .removeFrom(this.flightPlanLayer())
        .removeFrom(allFlightPlansLayer);
    }
    this.markers = [];
    if (this.path != null) {
      this.path
        .removeFrom(selectedFlightPlansLayer)
        .removeFrom(this.flightPlanLayer())
        .removeFrom(allFlightPlansLayer);
    }
  }

  drawFlightPlan() {
    this.clearFlightPlan();
    this.flight.flightIsInAto().then((inAto) => {
      if (!inAto) {
        // HACK: The signal to redraw the ATO following package/flight deletion
        // and the signal to change flight/package selection due to UI selection
        // change come in an arbitrary order. If redraw signal comes first the
        // UI will clear the map and redraw, but then when the UI updates
        // selection away from the (now deleted) flight/package it calls
        // deselect, which redraws the deleted flight plan in its deselected
        // state.
        //
        // Avoid this by checking that the flight is still in the coalition's
        // ATO before drawing.
        return;
      }
      const path = [];
      this.flightPlan.forEach((waypoint) => {
        if (waypoint.includeInPath()) {
          path.push(waypoint.position());
        }
        if (this.shouldMark(waypoint)) {
          waypoint.marker
            .addTo(selectedFlightPlansLayer)
            .addTo(this.flightPlanLayer())
            .addTo(allFlightPlansLayer);
          this.markers.push(waypoint.marker);
        }
      });

      this.drawPath(path);
    });
  }
}

function drawAircraft() {
  aircraftLayer.clearLayers();
  blueFlightPlansLayer.clearLayers();
  redFlightPlansLayer.clearLayers();
  selectedFlightPlansLayer.clearLayers();
  allFlightPlansLayer.clearLayers();
  let selected = null;
  game.flights.forEach((flight) => {
    // Draw the selected waypoint last so it's on top. bringToFront only brings
    // it to the front of the *extant* elements, so any flights drawn later will
    // be drawn on top. We could fight with manual Z-indexes but leaflet does a
    // lot of that automatically so it'd be error prone.
    if (flight.selected) {
      selected = flight;
    } else {
      new Flight(flight).draw();
    }
  });

  if (selected != null) {
    new Flight(selected).draw();
  }
}

function _drawThreatZones(zones, layer, player) {
  const color = player ? Colors.Blue : Colors.Red;
  for (const zone of zones) {
    L.polyline(zone, {
      color: color,
      weight: 1,
      fill: true,
      fillOpacity: 0.4,
      noClip: true,
      interactive: false,
    }).addTo(layer);
  }
}

function drawThreatZones() {
  blueFullThreatZones.clearLayers();
  blueAircraftThreatZones.clearLayers();
  blueAirDefenseThreatZones.clearLayers();
  blueRadarSamThreatZones.clearLayers();
  redFullThreatZones.clearLayers();
  redAircraftThreatZones.clearLayers();
  redAirDefenseThreatZones.clearLayers();
  redRadarSamThreatZones.clearLayers();

  _drawThreatZones(game.threatZones.blue.full, blueFullThreatZones, true);
  _drawThreatZones(
    game.threatZones.blue.aircraft,
    blueAircraftThreatZones,
    true
  );
  _drawThreatZones(
    game.threatZones.blue.airDefenses,
    blueAirDefenseThreatZones,
    true
  );
  _drawThreatZones(
    game.threatZones.blue.radarSams,
    blueRadarSamThreatZones,
    true
  );

  _drawThreatZones(game.threatZones.red.full, redFullThreatZones, false);
  _drawThreatZones(
    game.threatZones.red.aircraft,
    redAircraftThreatZones,
    false
  );
  _drawThreatZones(
    game.threatZones.red.airDefenses,
    redAirDefenseThreatZones,
    false
  );
  _drawThreatZones(
    game.threatZones.red.radarSams,
    redRadarSamThreatZones,
    false
  );
}

function drawNavmesh(zones, layer) {
  for (const zone of zones) {
    L.polyline(zone.poly, {
      color: "#000000",
      weight: 1,
      fillColor: zone.threatened ? "#ff0000" : "#00ff00",
      fill: true,
      fillOpacity: 0.1,
      noClip: true,
      interactive: false,
    }).addTo(layer);
  }
}

function drawNavmeshes() {
  blueNavmesh.clearLayers();
  redNavmesh.clearLayers();

  drawNavmesh(game.navmeshes.blue, blueNavmesh);
  drawNavmesh(game.navmeshes.red, redNavmesh);
}

function drawMapZones() {
  seaZones.clearLayers();
  inclusionZones.clearLayers();
  exclusionZones.clearLayers();

  for (const zone of game.mapZones.seaZones) {
    L.polygon(zone, {
      color: "#344455",
      fillColor: "#344455",
      fillOpacity: 1,
      interactive: false,
    }).addTo(seaZones);
  }

  for (const zone of game.mapZones.inclusionZones) {
    L.polygon(zone, {
      color: "#969696",
      fillColor: "#4b4b4b",
      fillOpacity: 1,
      interactive: false,
    }).addTo(inclusionZones);
  }

  for (const zone of game.mapZones.exclusionZones) {
    L.polygon(zone, {
      color: "#969696",
      fillColor: "#303030",
      fillOpacity: 1,
      interactive: false,
    }).addTo(exclusionZones);
  }
}

function drawUnculledZones() {
  unculledZones.clearLayers();

  for (const zone of game.unculledZones) {
    L.circle(zone.position, {
      radius: zone.radius,
      color: "#b4ff8c",
      fill: false,
      interactive: false,
    }).addTo(unculledZones);
  }
}

function drawIpZones() {
  ipZones.clearLayers();

  if (!ENABLE_EXPENSIVE_DEBUG_TOOLS) {
    return;
  }

  const iz = JSON.parse(game.ipZones);

  L.polygon(iz.homeBubble, {
    color: Colors.Highlight,
    fillOpacity: 0.1,
    interactive: false,
  }).addTo(ipZones);

  L.polygon(iz.ipBubble, {
    color: "#bb89ff",
    fillOpacity: 0.1,
    interactive: false,
  }).addTo(ipZones);

  L.polygon(iz.permissibleZone, {
    color: "#ffffff",
    fillOpacity: 0.1,
    interactive: false,
  }).addTo(ipZones);

  for (const zone of iz.safeZones) {
    L.polygon(zone, {
      color: Colors.Green,
      fillOpacity: 0.1,
      interactive: false,
    }).addTo(ipZones);
  }
}

function drawJoinZones() {
  joinZones.clearLayers();

  if (!ENABLE_EXPENSIVE_DEBUG_TOOLS) {
    return;
  }

  const jz = JSON.parse(game.joinZones);

  L.polygon(jz.homeBubble, {
    color: Colors.Highlight,
    fillOpacity: 0.1,
    interactive: false,
  }).addTo(joinZones);

  L.polygon(jz.targetBubble, {
    color: "#bb89ff",
    fillOpacity: 0.1,
    interactive: false,
  }).addTo(joinZones);

  L.polygon(jz.ipBubble, {
    color: "#ffffff",
    fillOpacity: 0.1,
    interactive: false,
  }).addTo(joinZones);

  for (const zone of jz.excludedZones) {
    L.polygon(zone, {
      color: "#ffa500",
      fillOpacity: 0.2,
      stroke: false,
      interactive: false,
    }).addTo(joinZones);
  }

  for (const zone of jz.permissibleZones) {
    L.polygon(zone, {
      color: Colors.Green,
      interactive: false,
    }).addTo(joinZones);
  }

  for (const line of jz.preferredLines) {
    L.polyline(line, {
      color: Colors.Green,
      interactive: false,
    }).addTo(joinZones);
  }
}

function drawHoldZones() {
  holdZones.clearLayers();

  if (!ENABLE_EXPENSIVE_DEBUG_TOOLS) {
    return;
  }

  const hz = JSON.parse(game.holdZones);

  L.polygon(hz.homeBubble, {
    color: Colors.Highlight,
    fillOpacity: 0.1,
    interactive: false,
  }).addTo(holdZones);

  L.polygon(hz.targetBubble, {
    color: Colors.Highlight,
    fillOpacity: 0.1,
    interactive: false,
  }).addTo(holdZones);

  L.polygon(hz.joinBubble, {
    color: Colors.Highlight,
    fillOpacity: 0.1,
    interactive: false,
  }).addTo(holdZones);

  for (const zone of hz.excludedZones) {
    L.polygon(zone, {
      color: "#ffa500",
      fillOpacity: 0.2,
      stroke: false,
      interactive: false,
    }).addTo(holdZones);
  }

  for (const zone of hz.permissibleZones) {
    L.polygon(zone, {
      color: Colors.Green,
      interactive: false,
    }).addTo(holdZones);
  }

  for (const line of hz.preferredLines) {
    L.polyline(line, {
      color: Colors.Green,
      interactive: false,
    }).addTo(holdZones);
  }
}

function drawCombat() {
  combatLayer.clearLayers();

  for (const airCombat of game.airCombats) {
    L.polygon(airCombat.footprint, {
      color: Colors.Red,
      interactive: false,
      fillOpacity: 0.2,
    }).addTo(combatLayer);
  }

  for (const samCombat of game.samCombats) {
    for (const airDefense of samCombat.airDefenses) {
      L.polyline([samCombat.flight.position, airDefense.position], {
        color: Colors.Red,
        interactive: false,
      }).addTo(combatLayer);
    }
  }

  for (const ipCombat of game.ipCombats) {
    L.polyline([ipCombat.flight.position, ipCombat.flight.target], {
      color: Colors.Red,
      interactive: false,
    }).addTo(combatLayer);
  }
}

function drawInitialMap() {
  recenterMap(game.mapCenter);
  drawControlPoints();
  drawGroundObjects();
  drawSupplyRoutes();
  drawFrontLines();
  drawAircraft();
  drawThreatZones();
  drawNavmeshes();
  drawMapZones();
  drawUnculledZones();
  drawIpZones();
  drawJoinZones();
  drawHoldZones();
  drawCombat();
}

function clearAllLayers() {
  map.eachLayer(function (layer) {
    if (layer.clearLayers !== undefined) {
      layer.clearLayers();
    }
  });
}

function setTooltipZoomThreshold(layerGroup, showAt) {
  let showing = map.getZoom() >= showAt;
  map.on("zoomend", function () {
    const zoom = map.getZoom();
    if (zoom < showAt && showing) {
      showing = false;
      layerGroup.eachLayer(function (layer) {
        if (layer.getTooltip()) {
          const tooltip = layer.getTooltip();
          layer.unbindTooltip().bindTooltip(tooltip, {
            permanent: false,
          });
        }
      });
    } else if (zoom >= showAt && !showing) {
      showing = true;
      layerGroup.eachLayer(function (layer) {
        if (layer.getTooltip()) {
          const tooltip = layer.getTooltip();
          layer.unbindTooltip().bindTooltip(tooltip, {
            permanent: true,
          });
        }
      });
    }
  });
}

setTooltipZoomThreshold(selectedFlightPlansLayer, SHOW_WAYPOINT_INFO_AT_ZOOM);
