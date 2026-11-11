import { HTTP_URL } from "../../api/backend";
import { renderWithProviders } from "../../testutils";
import WaypointMarker, { TOOLTIP_ZOOM_LEVEL } from "./WaypointMarker";
import { Map, Marker } from "leaflet";
import React from "react";
import { MapContainer } from "react-leaflet";
import { waitFor, fireEvent } from "@testing-library/react";
import { vi } from "vitest";

// Capture the trigger function calls for assertion.
// This mock avoids jsdom's incompatible AbortSignal with Node.js native Request
// which breaks RTK Query's fetchBaseQuery internally.
let triggerFn: jest.MockedFunction<any>;
vi.mock("../../api/liberationApi", () => ({
  liberationApi: vi.fn(),
  useSetWaypointPositionMutation: () => [triggerFn, {} as any],
}));

describe("WaypointMarker", () => {
  beforeEach(() => {
    triggerFn = vi.fn();
  });

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

  it("resets the tooltip while dragging", () => {
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
    marker.current?.fireEvent("dragstart");
    expect(marker.current?.getTooltip()?.getContent()).toEqual(
      "Waiting to recompute TOT..."
    );
  });

  it("sends the new position to the backend on dragend", async () => {
    const departure = {
      name: "",
      position: { lat: 0, lng: 0 },
      altitude_ft: 25000,
      altitude_reference: "MSL",
      is_movable: false,
      should_mark: false,
      include_in_path: true,
      timing: "09:00:00",
    };
    const waypoint = {
      name: "",
      position: { lat: 1, lng: 1 },
      altitude_ft: 25000,
      altitude_reference: "MSL",
      is_movable: false,
      should_mark: false,
      include_in_path: true,
      timing: "09:00:00",
    };
    const flight = {
      id: "1234",
      blue: true,
      sidc: "",
      waypoints: [departure, waypoint],
    };
    const marker = React.createRef<Marker>();

    renderWithProviders(
      <MapContainer>
        <WaypointMarker number={0} waypoint={departure} flight={flight} />
        <WaypointMarker
          number={1}
          waypoint={waypoint}
          flight={flight}
          ref={marker}
        />
      </MapContainer>
    );

    marker.current?.fireEvent("dragstart");
    marker.current?.fireEvent("dragend", { target: marker.current });

    // The dragend handler calls setWaypointPositionMutation (via RTK Query).
    await waitFor(() => expect(triggerFn).toHaveBeenCalledTimes(1), {
      timeout: 5000,
    });
    const [arg] = triggerFn.mock.calls[0];
    expect(arg.flightId).toBe(flight.id);
    expect(arg.waypointIdx).toBe(1);
  });
});
