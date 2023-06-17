import { renderWithProviders } from "../../testutils";
import NavMeshLayer from "./NavMeshLayer";
import { PropsWithChildren } from "react";

const mockPolygon = jest.fn();
const mockLayerGroup = jest.fn();
jest.mock("react-leaflet", () => ({
  LayerGroup: (props: PropsWithChildren<any>) => {
    mockLayerGroup(props);
    return <>{props.children}</>;
  },
  Polygon: (props: any) => {
    mockPolygon(props);
  },
}));

// The waypoints in test data below should all use `should_make: false`. Markers
// need useMap() to check the zoom level to decide if they should be drawn or
// not, and we don't have good options here for mocking that behavior.
describe("NavMeshLayer", () => {
  it("draws blue meshes", () => {
    const poly1 = [
      [
        { lat: -1, lng: 0 },
        { lat: 0, lng: 1 },
        { lat: 1, lng: 0 },
      ],
    ];
    const poly2 = [
      [
        { lat: -1, lng: 0 },
        { lat: 0, lng: -1 },
        { lat: 1, lng: 0 },
      ],
    ];
    renderWithProviders(<NavMeshLayer blue={true} />, {
      preloadedState: {
        navmeshes: {
          blue: [
            {
              poly: poly1,
              threatened: false,
            },
            {
              poly: poly2,
              threatened: true,
            },
          ],
          red: [
            {
              poly: [
                [
                  { lat: -1, lng: 0 },
                  { lat: 0, lng: 2 },
                  { lat: 1, lng: 0 },
                ],
              ],
              threatened: false,
            },
          ],
        },
      },
    });
    expect(mockPolygon).toHaveBeenCalledTimes(2);
    expect(mockPolygon).toHaveBeenCalledWith(
      expect.objectContaining({
        fillColor: "#00ff00",
        positions: poly1,
        interactive: false,
      })
    );
    expect(mockPolygon).toHaveBeenCalledWith(
      expect.objectContaining({
        fillColor: "#ff0000",
        positions: poly2,
        interactive: false,
      })
    );
    expect(mockLayerGroup).toHaveBeenCalledTimes(1);
  });
  it("draws red navmesh", () => {
    renderWithProviders(<NavMeshLayer blue={false} />, {
      preloadedState: {
        navmeshes: {
          blue: [
            {
              poly: [
                [
                  { lat: -1, lng: 0 },
                  { lat: 0, lng: 1 },
                  { lat: 1, lng: 0 },
                ],
              ],
              threatened: false,
            },
            {
              poly: [
                [
                  { lat: -1, lng: 0 },
                  { lat: 0, lng: -1 },
                  { lat: 1, lng: 0 },
                ],
              ],
              threatened: true,
            },
          ],
          red: [
            {
              poly: [
                [
                  { lat: -1, lng: 0 },
                  { lat: 0, lng: 2 },
                  { lat: 1, lng: 0 },
                ],
              ],
              threatened: false,
            },
          ],
        },
      },
    });
    expect(mockPolygon).toHaveBeenCalledTimes(1);
    expect(mockLayerGroup).toHaveBeenCalledTimes(1);
  });
});
