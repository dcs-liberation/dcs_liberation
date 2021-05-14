/*
 * TODO:
 *
 * - Culling
 * - Threat zones
 * - Navmeshes
 * - CV waypoints
 * - Time of day/weather themeing
 * - Exclusion zones
 * - Commit ranges
 * - Supply route status
 * - "Actual" front line
 * - Debug flight plan drawing
 * - Icon variety
 */

const Colors = Object.freeze({
  Blue: "#0084ff",
  Red: "#c85050",
});

var map = L.map("map").setView([0, 0], 3);
L.control.scale({ maxWidth: 200 }).addTo(map);

// https://esri.github.io/esri-leaflet/api-reference/layers/basemap-layer.html
var baseLayers = {
  "Imagery Clarity": L.esri.basemapLayer("ImageryClarity", { maxZoom: 17 }),
  "Imagery Firefly": L.esri.basemapLayer("ImageryFirefly", { maxZoom: 17 }),
};

var defaultBaseMap = baseLayers["Imagery Clarity"];
defaultBaseMap.addTo(map);

// Enabled by default, so addTo(map).
var controlPointsLayer = L.layerGroup().addTo(map);
var groundObjectsLayer = L.markerClusterGroup().addTo(map);
var supplyRoutesLayer = L.layerGroup().addTo(map);
var frontLinesLayer = L.layerGroup().addTo(map);
var redSamThreatLayer = L.layerGroup().addTo(map);
var blueFlightPlansLayer = L.layerGroup().addTo(map);

// Added to map by the user via layer controls.
var blueSamThreatLayer = L.layerGroup();
var blueSamDetectionLayer = L.layerGroup();
var redSamDetectionLayer = L.layerGroup();
var redFlightPlansLayer = L.layerGroup();
var selectedFlightPlansLayer = L.layerGroup();

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

var friendlyCpIcon = new L.Icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

var enemyCpIcon = new L.Icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

var game;
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

function drawControlPoints() {
  controlPointsLayer.clearLayers();
  var zoom = map.getZoom();
  game.controlPoints.forEach((cp) => {
    L.marker(cp.position, { icon: iconFor(cp.blue) })
      .bindTooltip(`<h3 style="margin: 0;">${cp.name}</h3>`, {
        permanent: zoom >= SHOW_BASE_NAME_AT_ZOOM,
      })
      .on("click", function () {
        cp.showInfoDialog();
      })
      .on("contextmenu", function () {
        cp.showPackageDialog();
      })
      .addTo(controlPointsLayer);
  });
}

function drawSamThreatsAt(tgo) {
  var detectionLayer = tgo.blue ? blueSamDetectionLayer : redSamDetectionLayer;
  var threatLayer = tgo.blue ? blueSamThreatLayer : redSamThreatLayer;
  var threatColor = tgo.blue ? Colors.Blue : Colors.Red;
  var detectionColor = tgo.blue ? "#bb89ff" : "#eee17b";

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
      weight: 1,
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
    var color;
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
  var layer = flight.blue ? blueFlightPlansLayer : redFlightPlansLayer;
  var color = flight.blue ? Colors.Blue : Colors.Red;
  var highlight = "#ffff00";
  // We don't need a marker for the departure waypoint (and it's likely
  // coincident with the landing waypoint, so hard to see). We do want to draw
  // the path from it though.
  var points = [flight.flightPlan[0].position];
  var zoom = map.getZoom();
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
    L.polyline(points, { color: highlight }).addTo(selectedFlightPlansLayer);
    L.polyline(points, { color: highlight }).addTo(layer);
  } else {
    L.polyline(points, { color: color, weight: 1 }).addTo(layer);
  }
}

function drawFlightPlans() {
  blueFlightPlansLayer.clearLayers();
  redFlightPlansLayer.clearLayers();
  selectedFlightPlansLayer.clearLayers();
  var selected = null;
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
  var showing = map.getZoom() >= showAt;
  map.on("zoomend", function () {
    var zoom = map.getZoom();
    if (zoom < showAt && showing) {
      showing = false;
      layerGroup.eachLayer(function (layer) {
        if (layer.getTooltip()) {
          var tooltip = layer.getTooltip();
          layer.unbindTooltip().bindTooltip(tooltip, {
            permanent: false,
          });
        }
      });
    } else if (zoom >= showAt && !showing) {
      showing = true;
      layerGroup.eachLayer(function (layer) {
        if (layer.getTooltip()) {
          var tooltip = layer.getTooltip();
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
