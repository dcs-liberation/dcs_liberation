import { renderWithProviders } from "../../testutils";
import FrontLinesLayer from "./FrontLinesLayer";
import { PropsWithChildren } from "react";
import { vi } from "vitest";

const mockPolyline = jest.fn();
const mockLayerGroup = jest.fn();
vi.mock("react-leaflet", () => ({
  LayerGroup: (props: PropsWithChildren<object>) => {
    mockLayerGroup(props);
    return <>{props.children}</>;
  },
  Polyline: (props: React.ComponentProps<"polyline">) => {
    mockPolyline(props);
  },
}));

// The waypoints in test data below should all use `should_make: false`. Markers
// need useMap() to check the zoom level to decide if they should be drawn or
// not, and we don't have good options here for mocking that behavior.
describe("FrontLinesLayer", () => {
  it("draws nothing when there are no front lines", () => {
    renderWithProviders(<FrontLinesLayer />);
    expect(mockPolyline).not.toHaveBeenCalled();
    expect(mockLayerGroup).toHaveBeenCalledTimes(1);
  });

  it("draws front lines", () => {
    const extents = [
      { lat: 0, lng: 0 },
      { lat: 1, lng: 1 },
    ];
    renderWithProviders(<FrontLinesLayer />, {
      preloadedState: {
        frontLines: {
          fronts: {
            foo: {
              id: "foo",
              extents: extents,
            },
            bar: {
              id: "bar",
              extents: extents,
            },
          },
        },
      },
    });
    expect(mockPolyline).toHaveBeenCalledTimes(2);
    expect(mockPolyline).toHaveBeenCalledWith(
      expect.objectContaining({
        positions: extents,
      })
    );
    expect(mockLayerGroup).toHaveBeenCalledTimes(1);
  });
});
