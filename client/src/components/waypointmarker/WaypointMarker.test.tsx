import { renderWithProviders } from "../../testutils";
import WaypointMarker, { TOOLTIP_ZOOM_LEVEL } from "./WaypointMarker";
import { Map, Marker } from "leaflet";
import React from "react";
import { MapContainer } from "react-leaflet";

describe("WaypointMarker", () => {
  it("is placed in the correct location", () => {
    const waypoint = {
      name: "",
      position: { lat: 0, lng: 0 },
      altitude_ft: 0,
      altitude_reference: "MSL",
      is_movable: false,
      should_mark: false,
      include_in_path: true,
      timing: "",
    };
    const marker = React.createRef<Marker>();
    renderWithProviders(
      <MapContainer>
        <WaypointMarker
          number={0}
          waypoint={waypoint}
          flight={{
            id: "",
            blue: true,
            sidc: "",
            waypoints: [waypoint],
          }}
          ref={marker}
        />
      </MapContainer>
    );
    expect(marker.current?.getLatLng()).toEqual({ lat: 0, lng: 0 });
  });

  it("tooltip is hidden when zoomed out", () => {
    const waypoint = {
      name: "",
      position: { lat: 0, lng: 0 },
      altitude_ft: 0,
      altitude_reference: "MSL",
      is_movable: false,
      should_mark: false,
      include_in_path: true,
      timing: "",
    };
    const map = React.createRef<Map>();
    const marker = React.createRef<Marker>();
    renderWithProviders(
      <MapContainer zoom={0} ref={map}>
        <WaypointMarker
          number={0}
          waypoint={waypoint}
          flight={{
            id: "",
            blue: true,
            sidc: "",
            waypoints: [waypoint],
          }}
          ref={marker}
        />
      </MapContainer>
    );
    map.current?.setView({ lat: 0, lng: 0 }, TOOLTIP_ZOOM_LEVEL - 1);
    expect(marker.current?.getTooltip()?.isOpen()).toBeFalsy();
  });

  it("tooltip is shown when zoomed in", () => {
    const waypoint = {
      name: "",
      position: { lat: 0, lng: 0 },
      altitude_ft: 0,
      altitude_reference: "MSL",
      is_movable: false,
      should_mark: false,
      include_in_path: true,
      timing: "",
    };
    const map = React.createRef<Map>();
    const marker = React.createRef<Marker>();
    renderWithProviders(
      <MapContainer ref={map}>
        <WaypointMarker
          number={0}
          waypoint={waypoint}
          flight={{
            id: "",
            blue: true,
            sidc: "",
            waypoints: [waypoint],
          }}
          ref={marker}
        />
      </MapContainer>
    );
    map.current?.setView({ lat: 0, lng: 0 }, TOOLTIP_ZOOM_LEVEL);
    expect(marker.current?.getTooltip()?.isOpen()).toBeTruthy();
  });

  it("tooltip has correct contents", () => {
    const waypoint = {
      name: "",
      position: { lat: 0, lng: 0 },
      altitude_ft: 25000,
      altitude_reference: "MSL",
      is_movable: false,
      should_mark: false,
      include_in_path: true,
      timing: "09:00:00",
    };
    const map = React.createRef<Map>();
    const marker = React.createRef<Marker>();
    renderWithProviders(
      <MapContainer ref={map}>
        <WaypointMarker
          number={0}
          waypoint={waypoint}
          flight={{
            id: "",
            blue: true,
            sidc: "",
            waypoints: [waypoint],
          }}
          ref={marker}
        />
      </MapContainer>
    );
    expect(marker.current?.getTooltip()?.getContent()).toEqual(
      "0 <br />25000 ft MSL<br />09:00:00"
    );
  });
});
