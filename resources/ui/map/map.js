const ENABLE_EXPENSIVE_DEBUG_TOOLS = false;
// Must be kept in sync with game.server.settings.ServerSettings.
const HTTP_BACKEND = "http://[::1]:5000";
const WS_BACKEND = "ws://[::1]:5000/eventstream";

METERS_TO_FEET = 3.28084;

// Uniquely generated at startup and passed to use by the QWebChannel.
var API_KEY = null;

function getJson(endpoint) {
  return fetch(`${HTTP_BACKEND}${endpoint}`, {
    headers: {
      "X-API-Key": API_KEY,
    },
  }).then((response) => response.json());
}

function postJson(endpoint, data) {
  return fetch(`${HTTP_BACKEND}${endpoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
    },
    body: JSON.stringify(data),
  }).then((response) => response.json());
}

const Colors = Object.freeze({
  Blue: "#0084ff",
  Red: "#c85050",
  Green: "#80BA80",
  Highlight: "#ffff00",
});

function milSymbolIcon(sidc, options = {}) {
  const symbol = new ms.Symbol(sidc, options);
  return L.icon({
    iconUrl: symbol.toDataURL(),
    iconAnchor: L.point(symbol.getAnchor().x, symbol.getAnchor().y),
  });
}

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
  const ws = new WebSocket(WS_BACKEND);
  ws.addEventListener("message", (event) => {
    handleStreamedEvents(JSON.parse(event.data));
  });
  ws.addEventListener("close", (event) => {
    console.log(`Websocket closed: ${event}`);
  });
  ws.addEventListener("error", (error) => {
    console.log(`Websocket error: ${error}`);
  });

  game = channel.objects.game;
  API_KEY = game.apiKey;
  drawInitialMap();
  game.cleared.connect(clearAllLayers);
  game.mapCenterChanged.connect(recenterMap);
  game.controlPointsChanged.connect(drawControlPoints);
  game.groundObjectsChanged.connect(drawGroundObjects);
  game.supplyRoutesChanged.connect(drawSupplyRoutes);
  game.mapReset.connect(drawAircraft);
});

function handleStreamedEvents(events) {
  for (const [flightId, position] of Object.entries(
    events.updated_flight_positions
  )) {
    Flight.withId(flightId).updatePosition(position);
  }

  for (const combat of events.new_combats) {
    redrawCombat(combat);
  }

  for (const combat of events.updated_combats) {
    redrawCombat(combat);
  }

  for (const combatId of events.ended_combats) {
    clearCombat(combatId);
  }

  for (const player of events.navmesh_updates) {
    drawNavmesh(player);
  }

  if (events.unculled_zones_updated) {
    drawUnculledZones();
  }

  if (events.threat_zones_updated) {
    drawThreatZones();
  }

  if (events.deselected_flight && Flight.selected != null) {
    Flight.deselectCurrent();
  }

  if (events.selected_flight != null) {
    Flight.select(events.selected_flight);
  }

  for (const flight of events.new_flights) {
    new Flight(flight).draw();
  }

  for (const flightId of events.updated_flights) {
    Flight.withId(flightId).draw();
  }

  for (const flightId of events.deleted_flights) {
    Flight.popId(flightId).clear();
  }
}

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
    return milSymbolIcon(this.cp.sidc, {
      size: 24,
      colorMode: "Dark",
    });
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

  icon() {
    return milSymbolIcon(this.tgo.sidc, { size: 24 });
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
  getJson("/front-lines").then((frontLines) => {
    for (const front of frontLines) {
      L.polyline(front.extents, { weight: 8, color: "#fe7d0a" })
        .on("contextmenu", function () {
          front.showPackageDialog();
        })
        .addTo(frontLinesLayer);
    }
  });
}

const SHOW_WAYPOINT_INFO_AT_ZOOM = 9;

class Waypoint {
  constructor(waypoint, number, flight) {
    this.waypoint = waypoint;
    this.number = number;
    this.flight = flight;
    this.marker = this.makeMarker();
  }

  position() {
    return this.waypoint.position;
  }

  shouldMark() {
    return this.waypoint.should_mark;
  }

  async timing(dragging) {
    if (dragging) {
      return "Waiting to recompute TOT...";
    }
    return await getJson(`/waypoints/${this.flight.id}/${this.number}/timing`);
  }

  async description(dragging) {
    const alt = this.waypoint.altitude_ft;
    const altRef = this.waypoint.altitude_reference;
    return (
      `${this.number} ${this.waypoint.name}<br />` +
      `${alt} ft ${altRef}<br />` +
      `${await this.timing(dragging)}`
    );
  }

  relocate() {
    this.marker.setLatLng(this.position());
  }

  updateDescription(dragging) {
    this.description(dragging).then((description) => {
      this.marker.setTooltipContent(description);
    });
  }

  makeMarker() {
    const zoom = map.getZoom();
    const marker = L.marker(this.position(), {
      draggable: this.waypoint.is_movable,
    })
      .on("dragstart", (e) => {
        this.updateDescription(true);
      })
      .on("drag", (e) => {
        const marker = e.target;
        const destination = marker.getLatLng();
        this.flight.updatePath(this.number, destination);
      })
      .on("dragend", (e) => {
        const marker = e.target;
        const destination = marker.getLatLng();
        postJson(
          `/waypoints/${this.flight.id}/${this.number}/position`,
          destination
        )
          .then(() => {
            this.waypoint.position = destination;
            this.updateDescription(false);
            this.flight.drawCommitBoundary();
          })
          .catch((err) => {
            if (err) {
              this.relocate();
              console.log(err);
              marker.bindPopup(`${err}`).openPopup();
            }
          });
      });

    this.description(false).then((description) =>
      marker.bindTooltip(description, {
        permanent: zoom >= SHOW_WAYPOINT_INFO_AT_ZOOM,
      })
    );

    return marker;
  }

  includeInPath() {
    return this.waypoint.include_in_path;
  }
}

class Flight {
  static registeredFlights = {};
  static selected = null;

  constructor(flight) {
    this.flight = flight;
    this.id = flight.id;
    this.selected = false;
    self.position = flight.position;
    this.aircraft = null;
    this.path = null;
    this.markers = [];
    this.commitBoundary = null;
    Flight.registerFlight(this);
  }

  static clearRegisteredFlights() {
    Flight.registeredFlights = {};
  }

  static registerFlight(flight) {
    Flight.registeredFlights[flight.id] = flight;
  }

  static unregisterFlight(id) {
    if (Flight.selected != null && Flight.selected.id == id) {
      Flight.clearSelected();
    }
    delete Flight.registeredFlights[id];
  }

  static withId(id) {
    return Flight.registeredFlights[id];
  }

  static popId(id) {
    const flight = Flight.withId(id);
    Flight.unregisterFlight(id);
    return flight;
  }

  static clearSelected() {
    holdZones.clearLayers();
    ipZones.clearLayers();
    joinZones.clearLayers();
    Flight.selected = null;
  }

  static deselectCurrent() {
    const flight = Flight.selected;
    Flight.clearSelected();
    if (flight != null) {
      flight.selected = false;
      flight.draw();
    }
  }

  static select(id) {
    if (Flight.selected != null && Flight.selected.id == id) {
      return;
    }

    Flight.deselectCurrent();
    const flight = Flight.withId(id);
    Flight.selected = flight;
    flight.selected = true;
    flight.draw();
    drawHoldZones(id);
    drawIpZones(id);
    drawJoinZones(id);
  }

  shouldMark(waypoint) {
    return this.selected && waypoint.shouldMark();
  }

  flightPlanLayer() {
    return this.flight.blue ? blueFlightPlansLayer : redFlightPlansLayer;
  }

  updatePosition(position) {
    this.position = position;
    this.drawAircraftLocation();
  }

  updatePath(idx, position) {
    const points = this.path.getLatLngs();
    points[idx] = position;
    this.path.setLatLngs(points);
  }

  drawPath(path) {
    const color = this.flight.blue ? Colors.Blue : Colors.Red;
    const layer = this.flightPlanLayer();
    if (this.selected) {
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

  clear() {
    this.clearAircraftLocation();
    this.clearFlightPlan();
    this.clearCommitBoundary();
  }

  clearAircraftLocation() {
    if (this.aircraft != null) {
      this.aircraft.removeFrom(aircraftLayer);
      this.aircraft = null;
    }
  }

  drawAircraftLocation() {
    this.clearAircraftLocation();
    if (this.position != null) {
      this.aircraft = L.marker(this.position, {
        icon: milSymbolIcon(this.flight.sidc, { size: 16 }),
      }).addTo(aircraftLayer);
    }
  }

  clearCommitBoundary() {
    if (this.commitBoundary != null) {
      this.commitBoundary
        .removeFrom(selectedFlightPlansLayer)
        .removeFrom(this.flightPlanLayer())
        .removeFrom(allFlightPlansLayer);
    }
  }

  drawCommitBoundary() {
    if (!this.selected) {
      this.clearCommitBoundary();
      return;
    }

    getJson(`/flights/${this.flight.id}/commit-boundary`).then((boundary) => {
      // For a selected flight we wait to clear the commit boundary until after
      // the backend responds. Otherwise if the package is reselected while
      // waiting we may have the following execution order, with selections A
      // and B:
      //
      // 1. A: clear
      // 2. A: wait for backend
      // 3. B: wait for backend
      // 4. A: Add boundary to map
      // 5. B: Add boundary to map
      //
      // Similarly, we need to recheck that we're still selected before
      // continuing.
      this.clearCommitBoundary();
      if (boundary && this.selected) {
        this.commitBoundary = L.polyline(boundary, {
          color: Colors.Highlight,
          weight: 1,
          interactive: false,
        })
          .addTo(selectedFlightPlansLayer)
          .addTo(this.flightPlanLayer())
          .addTo(allFlightPlansLayer);
      }
    });
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
    const path = [];
    this.flight.waypoints.map((raw, idx) => {
      const waypoint = new Waypoint(raw, idx, this);
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
  }
}

function drawAircraft() {
  Flight.clearRegisteredFlights();
  aircraftLayer.clearLayers();
  blueFlightPlansLayer.clearLayers();
  redFlightPlansLayer.clearLayers();
  selectedFlightPlansLayer.clearLayers();
  allFlightPlansLayer.clearLayers();

  getJson("/flights?with_waypoints=true").then((flights) => {
    for (const flight of flights) {
      new Flight(flight).draw();
    }
  });
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

  getJson("/map-zones/threats").then((threats) => {
    _drawThreatZones(threats.blue.full, blueFullThreatZones, true);
    _drawThreatZones(threats.blue.aircraft, blueAircraftThreatZones, true);
    _drawThreatZones(
      threats.blue.air_defenses,
      blueAirDefenseThreatZones,
      true
    );
    _drawThreatZones(threats.blue.radar_sams, blueRadarSamThreatZones, true);

    _drawThreatZones(threats.red.full, redFullThreatZones, false);
    _drawThreatZones(threats.red.aircraft, redAircraftThreatZones, false);
    _drawThreatZones(threats.red.air_defenses, redAirDefenseThreatZones, false);
    _drawThreatZones(threats.red.radar_sams, redRadarSamThreatZones, false);
  });
}

function drawNavmesh(player) {
  const layer = player ? blueNavmesh : redNavmesh;
  layer.clearLayers();
  getJson(`/navmesh?for_player=${player}`).then((zones) => {
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
  });
}

function drawNavmeshes() {
  drawNavmesh(true);
  drawNavmesh(false);
}

function drawMapZones() {
  seaZones.clearLayers();
  inclusionZones.clearLayers();
  exclusionZones.clearLayers();

  getJson("/map-zones/terrain").then((zones) => {
    for (const zone of zones.sea) {
      L.polygon(zone, {
        color: "#344455",
        fillColor: "#344455",
        fillOpacity: 1,
        interactive: false,
      }).addTo(seaZones);
    }

    for (const zone of zones.inclusion) {
      L.polygon(zone, {
        color: "#969696",
        fillColor: "#4b4b4b",
        fillOpacity: 1,
        interactive: false,
      }).addTo(inclusionZones);
    }

    for (const zone of zones.exclusion) {
      L.polygon(zone, {
        color: "#969696",
        fillColor: "#303030",
        fillOpacity: 1,
        interactive: false,
      }).addTo(exclusionZones);
    }
  });
}

function drawUnculledZones() {
  unculledZones.clearLayers();

  getJson("/map-zones/unculled").then((zones) => {
    for (const zone of zones) {
      L.circle(zone.position, {
        radius: zone.radius,
        color: "#b4ff8c",
        fill: false,
        interactive: false,
      }).addTo(unculledZones);
    }
  });
}

function drawIpZones(id) {
  ipZones.clearLayers();

  if (!ENABLE_EXPENSIVE_DEBUG_TOOLS) {
    return;
  }

  getJson(`/debug/waypoint-geometries/ip/${id}`).then((iz) => {
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
  });
}

function drawJoinZones(id) {
  joinZones.clearLayers();

  if (!ENABLE_EXPENSIVE_DEBUG_TOOLS) {
    return;
  }

  getJson(`/debug/waypoint-geometries/join/${id}`).then((jz) => {
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
  });
}

function drawHoldZones(id) {
  holdZones.clearLayers();

  if (!ENABLE_EXPENSIVE_DEBUG_TOOLS) {
    return;
  }

  getJson(`/debug/waypoint-geometries/hold/${id}`).then((hz) => {
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
  });
}

var COMBATS = {};

function clearCombat(id) {
  if (id in COMBATS) {
    for (const layer of COMBATS[id]) {
      layer.removeFrom(combatLayer);
    }
    delete COMBATS[id];
  }
}

function redrawCombat(combat) {
  clearCombat(combat.id);

  const layers = [];

  if (combat.footprint) {
    layers.push(
      L.polygon(combat.footprint, {
        color: Colors.Red,
        interactive: false,
        fillOpacity: 0.2,
      }).addTo(combatLayer)
    );
  }

  if (combat.flight_position) {
    for (target_position of combat.target_positions) {
      layers.push(
        L.polyline([combat.flight_position, target_position], {
          color: Colors.Red,
          interactive: false,
        }).addTo(combatLayer)
      );
    }
  }

  COMBATS[combat.id] = layers;
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
