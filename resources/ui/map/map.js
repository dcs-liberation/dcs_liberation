/*
 * TODO:
 *
 * - Culling
 * - Threat zones
 * - Navmeshes
 * - Time of day/weather themeing
 * - Exclusion zones
 * - Supply route status
 * - "Actual" front line
 * - Debug flight plan drawing
 * - Icon variety
 */

const Colors = Object.freeze({
  Blue: "#0084ff",
  Red: "#c85050",
  Green: "#80BA80",
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

const map = L.map("map").setView([0, 0], 3);
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
const groundObjectsLayer = L.markerClusterGroup({ maxClusterRadius: 40 }).addTo(
  map
);
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
      "Air Defenses": {
        "Ally SAM threat range": blueSamThreatLayer,
        "Enemy SAM threat range": redSamThreatLayer,
        "Ally SAM detection range": blueSamDetectionLayer,
        "Enemy SAM detection range": redSamDetectionLayer,
      },
      "Flight Plans": {
        Hide: L.layerGroup(),
        "Show selected blue": selectedFlightPlansLayer,
        "Show all blue": blueFlightPlansLayer,
        "Show all red": redFlightPlansLayer,
      },
    },
    { collapsed: false, exclusiveGroups: ["Flight Plans"] }
  )
  .addTo(map);

const friendlyCpIcon = new L.Icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

const enemyCpIcon = new L.Icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

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

function iconFor(player) {
  if (player) {
    return friendlyCpIcon;
  } else {
    return enemyCpIcon;
  }
}

const SHOW_BASE_NAME_AT_ZOOM = 8;

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
    const zoom = map.getZoom();
    const locationMarker = this.locationMarker(dragging);
    const destinationMarker = this.destinationMarker();
    locationMarker
      .bindTooltip(`<h3 style="margin: 0;">${this.cp.name}</h3>`, {
        permanent: zoom >= SHOW_BASE_NAME_AT_ZOOM,
      })
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
      icon: iconFor(this.cp.blue),
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
      icon: iconFor(this.cp.blue),
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

function drawSamThreatsAt(tgo) {
  const detectionLayer = tgo.blue
    ? blueSamDetectionLayer
    : redSamDetectionLayer;
  const threatLayer = tgo.blue ? blueSamThreatLayer : redSamThreatLayer;
  const threatColor = tgo.blue ? Colors.Blue : Colors.Red;
  const detectionColor = tgo.blue ? "#bb89ff" : "#eee17b";

  tgo.samDetectionRanges.forEach((range) => {
    L.circle(tgo.position, {
      radius: range,
      color: detectionColor,
      fill: false,
      weight: 1,
    }).addTo(detectionLayer);
  });

  tgo.samThreatRanges.forEach((range) => {
    L.circle(tgo.position, {
      radius: range,
      color: threatColor,
      fill: false,
      weight: 2,
    }).addTo(threatLayer);
  });
}

function drawGroundObjects() {
  groundObjectsLayer.clearLayers();
  blueSamDetectionLayer.clearLayers();
  redSamDetectionLayer.clearLayers();
  blueSamThreatLayer.clearLayers();
  redSamThreatLayer.clearLayers();
  game.groundObjects.forEach((tgo) => {
    L.marker(tgo.position, { icon: iconFor(tgo.blue) })
      .bindTooltip(`${tgo.name}<br />${tgo.units.join("<br />")}`)
      .on("click", function () {
        tgo.showInfoDialog();
      })
      .on("contextmenu", function () {
        tgo.showPackageDialog();
      })
      .addTo(groundObjectsLayer);
    drawSamThreatsAt(tgo);
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
    L.polyline(route.points, {
      color: color,
      weight: route.isSea ? 4 : 6,
    }).addTo(supplyRoutesLayer);
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

function drawFlightPlan(flight) {
  const layer = flight.blue ? blueFlightPlansLayer : redFlightPlansLayer;
  const color = flight.blue ? Colors.Blue : Colors.Red;
  const highlight = "#ffff00";
  // We don't need a marker for the departure waypoint (and it's likely
  // coincident with the landing waypoint, so hard to see). We do want to draw
  // the path from it though.
  const points = [flight.flightPlan[0].position];
  const zoom = map.getZoom();
  flight.flightPlan.slice(1).forEach((waypoint) => {
    if (!waypoint.isDivert) {
      points.push(waypoint.position);
    }

    if (flight.selected) {
      L.marker(waypoint.position)
        .bindTooltip(
          `${waypoint.number} ${waypoint.name}<br />` +
            `${waypoint.altitudeFt} ft ${waypoint.altitudeReference}<br />` +
            `${waypoint.timing}`,
          { permanent: zoom >= SHOW_WAYPOINT_INFO_AT_ZOOM }
        )
        .addTo(layer)
        .addTo(selectedFlightPlansLayer);
    }
  });

  if (flight.selected) {
    L.polyline(points, { color: highlight })
      .addTo(layer)
      .addTo(selectedFlightPlansLayer);
    if (flight.commitBoundary) {
      L.polyline(flight.commitBoundary, { color: highlight, weight: 1 }).addTo(
        layer.addTo(selectedFlightPlansLayer)
      );
    }
  } else {
    L.polyline(points, { color: color, weight: 1 }).addTo(layer);
  }
}

function drawFlightPlans() {
  blueFlightPlansLayer.clearLayers();
  redFlightPlansLayer.clearLayers();
  selectedFlightPlansLayer.clearLayers();
  let selected = null;
  game.flights.forEach((flight) => {
    // Draw the selected waypoint last so it's on top. bringToFront only brings
    // it to the front of the *extant* elements, so any flights drawn later will
    // be drawn on top. We could fight with manual Z-indexes but leaflet does a
    // lot of that automatically so it'd be error prone.
    if (flight.selected) {
      selected = flight;
    } else {
      drawFlightPlan(flight);
    }
  });

  if (selected != null) {
    drawFlightPlan(selected);
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

setTooltipZoomThreshold(controlPointsLayer, SHOW_BASE_NAME_AT_ZOOM);
setTooltipZoomThreshold(selectedFlightPlansLayer, SHOW_WAYPOINT_INFO_AT_ZOOM);
