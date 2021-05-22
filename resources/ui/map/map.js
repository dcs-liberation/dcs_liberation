/*
 * TODO:
 *
 * - Culling
 * - Threat zones
 * - Navmeshes
 * - Time of day/weather themeing
 * - Exclusion zones
 * - "Actual" front line
 * - Debug flight plan drawing
 */

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
  "fob",
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
          fob: this.loadLegacyIcon(player),
          lha: this.loadIcon("lha", player, state),
          offmap: this.loadLegacyIcon(player),
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

  loadLegacyIcon(player) {
    const color = player ? "blue" : "red";
    return new L.Icon({
      iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color}.png`,
      shadowUrl:
        "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41],
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

const Icons = Object.freeze({
  ControlPoints: new CpIcons(),
  Objectives: new TgoIcons(),
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

const map = L.map("map", { doubleClickZoom: false }).setView([0, 0], 3);
L.control.scale({ maxWidth: 200 }).addTo(map);

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
const groundObjectsLayer = L.layerGroup().addTo(map);
const supplyRoutesLayer = L.layerGroup().addTo(map);
const frontLinesLayer = L.layerGroup().addTo(map);
const redSamThreatLayer = L.layerGroup().addTo(map);
const blueFlightPlansLayer = L.layerGroup().addTo(map);

// Added to map by the user via layer controls.
const blueSamThreatLayer = L.layerGroup();
const blueSamDetectionLayer = L.layerGroup();
const redSamDetectionLayer = L.layerGroup();
const redFlightPlansLayer = L.layerGroup();
const selectedFlightPlansLayer = L.layerGroup();
const allFlightPlansLayer = L.layerGroup();

L.control
  .groupedLayers(
    baseLayers,
    {
      "Points of Interest": {
        "Control points": controlPointsLayer,
        "Ground objects": groundObjectsLayer,
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
    { collapsed: false, exclusiveGroups: ["Flight Plans"] }
  )
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
  game.flightsChanged.connect(drawFlightPlans);
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
    // TODO: Runway status.
    // https://github.com/dcs-liberation/dcs_liberation/issues/1105
    return Icons.ControlPoints.icon(
      this.cp.category,
      this.cp.blue,
      UnitState.Alive
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
    });
  }

  onDestinationChanged() {
    if (this.hasDestination()) {
      this.primaryMarker.setLatLng(this.cp.destination);
      this.secondaryMarker.addTo(controlPointsLayer);
      this.path.setLatLngs([this.cp.position, this.cp.destination]);
      this.path.addTo(controlPointsLayer);
      this.path.setStyle({ color: Colors.Green });
    } else {
      this.hideDestination();
      this.primaryMarker.setLatLng(this.cp.position);
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
      }).addTo(detectionLayer);
    });

    this.tgo.samThreatRanges.forEach((range) => {
      L.circle(this.tgo.position, {
        radius: range,
        color: threatColor,
        fill: false,
        weight: 2,
      }).addTo(threatLayer);
    });
  }

  draw() {
    L.marker(this.tgo.position, { icon: this.icon() })
      .bindTooltip(`${this.tgo.name}<br />${this.tgo.units.join("<br />")}`)
      .on("click", () => this.tgo.showInfoDialog())
      .on("contextmenu", () => this.tgo.showPackageDialog())
      .addTo(groundObjectsLayer);
    this.drawSamThreats();
  }
}

function drawGroundObjects() {
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
    return !this.waypoint.isTakeoff;
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
    return L.marker(this.waypoint.position, { draggable: true })
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
    this.path = null;
    this.commitBoundary = null;
    this.flight.flightPlanChanged.connect(() => this.draw());
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
      this.path = L.polyline(path, { color: Colors.Highlight })
        .addTo(selectedFlightPlansLayer)
        .addTo(layer)
        .addTo(allFlightPlansLayer);
    } else {
      this.path = L.polyline(path, { color: color })
        .addTo(layer)
        .addTo(allFlightPlansLayer);
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
        })
          .addTo(selectedFlightPlansLayer)
          .addTo(this.flightPlanLayer())
          .addTo(allFlightPlansLayer);
      }
    }
  }

  draw() {
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
      }
    });

    this.drawPath(path);
    this.drawCommitBoundary();
  }
}

function drawFlightPlans() {
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

function drawInitialMap() {
  recenterMap(game.mapCenter);
  drawControlPoints();
  drawGroundObjects();
  drawSupplyRoutes();
  drawFrontLines();
  drawFlightPlans();
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
