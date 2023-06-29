import { HTTP_URL } from "../../api/backend";
import { renderWithProviders } from "../../testutils";
import WaypointMarker, { TOOLTIP_ZOOM_LEVEL } from "./WaypointMarker";
import { Map, Marker } from "leaflet";
import { rest, MockedRequest, matchRequestUrl } from "msw";
import { setupServer } from "msw/node";
import React from "react";
import { MapContainer } from "react-leaflet";

// https://mswjs.io/docs/extensions/life-cycle-events#asserting-request-payload
const waitForRequest = (method: string, url: string) => {
  let requestId = "";

  return new Promise<MockedRequest>((resolve, reject) => {
    server.events.on("request:start", (req) => {
      const matchesMethod = req.method.toLowerCase() === method.toLowerCase();
      const matchesUrl = matchRequestUrl(req.url, url).matches;

      if (matchesMethod && matchesUrl) {
        requestId = req.id;
      }
    });

    server.events.on("request:match", (req) => {
      if (req.id === requestId) {
        resolve(req);
      }
    });

    server.events.on("request:unhandled", (req) => {
      if (req.id === requestId) {
        reject(
          new Error(`The ${req.method} ${req.url.href} request was unhandled.`)
        );
      }
    });
  });
};

const server = setupServer(
  rest.post(
    `${HTTP_URL}/waypoints/:flightId/:waypointIdx/position`,
    (req, res, ctx) => {
      if (req.params.flightId === "") {
        return res(ctx.status(500));
      }
      if (req.params.waypointIdx === "0") {
        return res(ctx.status(403));
      }
      return res(ctx.status(204));
    }
  )
);

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

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

    // There is no observable UI change from moving a waypoint, just a message
    // to the backend to record the frontend change. The real backend will then
    // push an updated game state which will update redux, but that's not part
    // of this component's behavior.
    const pendingRequest = waitForRequest(
      "POST",
      `${HTTP_URL}/waypoints/1234/1/position`
    );

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

    const request = await pendingRequest;
    const response = await request.json();
    expect(response).toEqual({ lat: 1, lng: 1 });
  });
});
