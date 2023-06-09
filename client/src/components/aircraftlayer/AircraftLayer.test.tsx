import { renderWithProviders } from "../../testutils";
import AircraftLayer from "./AircraftLayer";
import { PropsWithChildren } from "react";

const mockLayerGroup = jest.fn();
const mockMarker = jest.fn();
jest.mock("react-leaflet", () => ({
  LayerGroup: (props: PropsWithChildren<any>) => {
    mockLayerGroup(props);
    return <>{props.children}</>;
  },
  Marker: (props: any) => {
    mockMarker(props);
  },
}));

test("layer is empty by default", async () => {
  renderWithProviders(<AircraftLayer />);
  expect(mockLayerGroup).toHaveBeenCalledTimes(1);
  expect(mockMarker).not.toHaveBeenCalled();
});

test("layer has aircraft if non-empty", async () => {
  renderWithProviders(<AircraftLayer />, {
    preloadedState: {
      flights: {
        flights: {
          foo: {
            id: "foo",
            blue: true,
            sidc: "",
            position: {
              lat: 0,
              lng: 0,
            },
          },
          bar: {
            id: "bar",
            blue: false,
            sidc: "",
            position: {
              lat: 0,
              lng: 0,
            },
          },
        },
        selected: null,
      },
    },
  });
  expect(mockLayerGroup).toHaveBeenCalledTimes(1);
  expect(mockMarker).toHaveBeenCalledTimes(2);
});
