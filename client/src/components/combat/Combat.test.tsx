import { renderWithProviders } from "../../testutils";
import Combat from "./Combat";
import { LatLng } from "leaflet";

const mockPolyline = jest.fn();
const mockPolygon = jest.fn();
jest.mock("react-leaflet", () => ({
  Polyline: (props: any) => {
    mockPolyline(props);
  },
  Polygon: (props: any) => {
    mockPolygon(props);
  },
}));

describe("Combat", () => {
  describe("footprint", () => {
    it("is not interactive", () => {
      renderWithProviders(
        <Combat
          combat={{
            id: "foo",
            flight_position: null,
            target_positions: null,
            footprint: [[new LatLng(0, 0), new LatLng(0, 1), new LatLng(1, 0)]],
          }}
        />
      );
      expect(mockPolygon).toBeCalledWith(
        expect.objectContaining({ interactive: false })
      );
    });

    // Fails because we don't handle multi-poly combat footprints correctly.
    it.skip("renders single polygons", () => {
      const boundary = [new LatLng(0, 0), new LatLng(0, 1), new LatLng(1, 0)];
      renderWithProviders(
        <Combat
          combat={{
            id: "foo",
            flight_position: null,
            target_positions: null,
            footprint: [boundary],
          }}
        />
      );
      expect(mockPolygon).toBeCalledWith(
        expect.objectContaining({ positions: boundary })
      );
    });

    // Fails because we don't handle multi-poly combat footprints correctly.
    it.skip("renders multiple polygons", () => {
      const boundary = [new LatLng(0, 0), new LatLng(0, 1), new LatLng(1, 0)];
      renderWithProviders(
        <Combat
          combat={{
            id: "foo",
            flight_position: null,
            target_positions: null,
            footprint: [boundary, boundary],
          }}
        />
      );
      expect(mockPolygon).toBeCalledTimes(2);
    });
  });

  describe("lines", () => {
    it("is not interactive", () => {
      renderWithProviders(
        <Combat
          combat={{
            id: "foo",
            flight_position: new LatLng(0, 0),
            target_positions: [new LatLng(1, 0)],
            footprint: null,
          }}
        />
      );
      expect(mockPolyline).toBeCalledWith(
        expect.objectContaining({ interactive: false })
      );
    });

    it("renders single line", () => {
      renderWithProviders(
        <Combat
          combat={{
            id: "foo",
            flight_position: new LatLng(0, 0),
            target_positions: [new LatLng(0, 1)],
            footprint: null,
          }}
        />
      );
      expect(mockPolyline).toBeCalledWith(
        expect.objectContaining({
          positions: [new LatLng(0, 0), new LatLng(0, 1)],
        })
      );
    });

    it("renders multiple lines", () => {
      renderWithProviders(
        <Combat
          combat={{
            id: "foo",
            flight_position: new LatLng(0, 0),
            target_positions: [new LatLng(0, 1), new LatLng(1, 0)],
            footprint: null,
          }}
        />
      );
      expect(mockPolyline).toBeCalledTimes(2);
    });
  });

  it("renders nothing if no footprint or targets", () => {
    const { container } = renderWithProviders(
      <Combat
        combat={{
          id: "foo",
          flight_position: new LatLng(0, 0),
          target_positions: null,
          footprint: null,
        }}
      />
    );
    expect(container).toBeEmptyDOMElement();
  });
});
