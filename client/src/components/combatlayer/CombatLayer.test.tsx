import { renderWithProviders } from "../../testutils";
import CombatLayer from "./CombatLayer";
import { LatLng } from "leaflet";
import { PropsWithChildren } from "react";

const mockPolyline = jest.fn();
const mockLayerGroup = jest.fn();
jest.mock("react-leaflet", () => ({
  LayerGroup: (props: PropsWithChildren<any>) => {
    mockLayerGroup(props);
    return <>{props.children}</>;
  },
  Polyline: (props: any) => {
    mockPolyline(props);
  },
}));

describe("CombatLayer", () => {
  it("renders each combat", () => {
    renderWithProviders(<CombatLayer />, {
      preloadedState: {
        combat: {
          combat: {
            foo: {
              id: "foo",
              flight_position: new LatLng(0, 0),
              target_positions: [new LatLng(0, 1)],
              footprint: null,
            },
            bar: {
              id: "foo",
              flight_position: new LatLng(0, 0),
              target_positions: [new LatLng(0, 1)],
              footprint: null,
            },
          },
        },
      },
    });
    expect(mockPolyline).toBeCalledTimes(2);
  });

  it("renders LayerGroup but no contents if no combat", () => {
    renderWithProviders(<CombatLayer />);
    expect(mockLayerGroup).toBeCalledTimes(1);
    expect(mockPolyline).not.toHaveBeenCalled();
  });
});
