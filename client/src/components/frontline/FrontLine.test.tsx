import { renderWithProviders } from "../../testutils";
import FrontLine from "./FrontLine";
import { PolylineProps } from "react-leaflet";

const mockPolyline = jest.fn();
jest.mock("react-leaflet", () => ({
  Polyline: (props: PolylineProps) => {
    mockPolyline(props);
  },
}));

describe("FrontLine", () => {
  it("is drawn in the correct location", () => {
    const extents = [
      { lat: 0, lng: 0 },
      { lat: 1, lng: 0 },
    ];
    renderWithProviders(
      <FrontLine
        front={{
          id: "",
          extents: extents,
        }}
      />
    );
    expect(mockPolyline).toHaveBeenCalledWith(
      expect.objectContaining({
        positions: extents,
      })
    );
  });
});
