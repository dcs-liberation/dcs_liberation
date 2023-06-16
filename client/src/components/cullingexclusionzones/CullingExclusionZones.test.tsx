import { renderWithProviders } from "../../testutils";
import CullingExclusionZones from "./CullingExclusionZones";
import { PropsWithChildren } from "react";

const mockCircle = jest.fn();
const mockLayerGroup = jest.fn();
const mockLayerControlOverlay = jest.fn();
jest.mock("react-leaflet", () => ({
  LayerGroup: (props: PropsWithChildren<any>) => {
    mockLayerGroup(props);
    return <>{props.children}</>;
  },
  LayersControl: {
    Overlay: (props: PropsWithChildren<any>) => {
      mockLayerControlOverlay(props);
      return <>{props.children}</>;
    },
  },
  Circle: (props: any) => {
    mockCircle(props);
  },
}));

describe("CullingExclusionZones", () => {
  it("is empty there are no exclusion zones", () => {
    renderWithProviders(<CullingExclusionZones />);
    expect(mockCircle).not.toHaveBeenCalled();
    expect(mockLayerGroup).toHaveBeenCalledTimes(1);
    expect(mockLayerControlOverlay).toHaveBeenCalledTimes(1);
  });

  describe("zone circles", () => {
    it("are drawn in the correct locations", () => {
      renderWithProviders(<CullingExclusionZones />, {
        preloadedState: {
          unculledZones: {
            zones: [
              {
                position: {
                  lat: 0,
                  lng: 0,
                },
                radius: 10,
              },
              {
                position: {
                  lat: 1,
                  lng: 1,
                },
                radius: 2,
              },
            ],
          },
        },
      });
      expect(mockCircle).toHaveBeenCalledTimes(2);
      expect(mockCircle).toHaveBeenCalledWith(
        expect.objectContaining({
          center: {
            lat: 0,
            lng: 0,
          },
          radius: 10,
        })
      );
      expect(mockCircle).toHaveBeenCalledWith(
        expect.objectContaining({
          center: {
            lat: 1,
            lng: 1,
          },
          radius: 2,
        })
      );
    });
    it("are not interactive", () => {});
  });
});
