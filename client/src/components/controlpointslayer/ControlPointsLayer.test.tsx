import { renderWithProviders } from "../../testutils";
import ControlPointsLayer from "./ControlPointsLayer";
import { LatLng } from "leaflet";
import { PropsWithChildren } from "react";
import { vi } from "vitest";

const mockMarker = jest.fn();
const mockLayerGroup = jest.fn();
vi.mock("react-leaflet", () => ({
  LayerGroup: (props: PropsWithChildren<object>) => {
    mockLayerGroup(props);
    return <>{props.children}</>;
  },
  Marker: (props: React.ComponentProps<"div">) => {
    mockMarker(props);
  },
  Tooltip: (props: PropsWithChildren<object>) => <div>{props.children}</div>,
  Polyline: (props: React.ComponentProps<"polyline">) => <polyline {...props} />,
}));

describe("ControlPointsLayer", () => {
  it("renders each control point", () => {
    renderWithProviders(<ControlPointsLayer />, {
      preloadedState: {
        controlPoints: {
          controlPoints: {
            foo: {
              id: "foo",
              name: "Foo",
              blue: true,
              position: new LatLng(0, 0),
              mobile: false,
              sidc: "",
            },
            bar: {
              id: "bar",
              name: "Bar",
              blue: false,
              position: new LatLng(1, 0),
              mobile: false,
              sidc: "",
            },
          },
        },
      },
    });
    expect(mockMarker).toBeCalledTimes(2);
  });

  it("renders LayerGroup but no contents if no combat", () => {
    renderWithProviders(<ControlPointsLayer />);
    expect(mockLayerGroup).toBeCalledTimes(1);
    expect(mockMarker).not.toHaveBeenCalled();
  });
});
