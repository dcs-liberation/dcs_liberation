import { renderWithProviders } from "../../testutils";
import AirDefenseRangeLayer, { colorFor } from "./AirDefenseRangeLayer";
import { PropsWithChildren } from "react";

const mockLayerGroup = jest.fn();
const mockCircle = jest.fn();
jest.mock("react-leaflet", () => ({
  LayerGroup: (props: PropsWithChildren<any>) => {
    mockLayerGroup(props);
    return <>{props.children}</>;
  },
  Circle: (props: any) => {
    mockCircle(props);
  },
}));

describe("colorFor", () => {
  it("has a unique color for each configuration", () => {
    const params = [
      [false, false],
      [false, true],
      [true, false],
      [true, true],
    ];
    var colors = new Set<string>();
    for (const [blue, detection] of params) {
      colors.add(colorFor(blue, detection));
    }
    expect(colors.size).toEqual(4);
  });
});

describe("AirDefenseRangeLayer", () => {
  it("draws nothing when there are no TGOs", () => {
    renderWithProviders(<AirDefenseRangeLayer blue={true} />);
    expect(mockLayerGroup).toHaveBeenCalledTimes(1);
    expect(mockCircle).not.toHaveBeenCalled();
  });

  it("does not draw wrong range types", () => {
    renderWithProviders(<AirDefenseRangeLayer blue={true} />, {
      preloadedState: {
        tgos: {
          tgos: {
            foo: {
              id: "foo",
              name: "Foo",
              control_point_name: "Bar",
              category: "AA",
              blue: false,
              position: {
                lat: 0,
                lng: 0,
              },
              units: [],
              threat_ranges: [],
              detection_ranges: [20],
              dead: false,
              sidc: "",
            },
          },
        },
      },
    });
    expect(mockLayerGroup).toHaveBeenCalledTimes(1);
    expect(mockCircle).not.toHaveBeenCalled();
  });

  it("draws threat ranges", () => {
    renderWithProviders(<AirDefenseRangeLayer blue={true} />, {
      preloadedState: {
        tgos: {
          tgos: {
            foo: {
              id: "foo",
              name: "Foo",
              control_point_name: "Bar",
              category: "AA",
              blue: true,
              position: {
                lat: 10,
                lng: 20,
              },
              units: [],
              threat_ranges: [10],
              detection_ranges: [20],
              dead: false,
              sidc: "",
            },
          },
        },
      },
    });
    expect(mockLayerGroup).toHaveBeenCalledTimes(1);
    expect(mockCircle).toHaveBeenCalledWith(
      expect.objectContaining({
        center: {
          lat: 10,
          lng: 20,
        },
        radius: 10,
        color: colorFor(true, false),
        interactive: false,
      })
    );
  });

  it("draws detection ranges", () => {
    renderWithProviders(<AirDefenseRangeLayer blue={true} detection />, {
      preloadedState: {
        tgos: {
          tgos: {
            foo: {
              id: "foo",
              name: "Foo",
              control_point_name: "Bar",
              category: "AA",
              blue: true,
              position: {
                lat: 10,
                lng: 20,
              },
              units: [],
              threat_ranges: [10],
              detection_ranges: [20],
              dead: false,
              sidc: "",
            },
          },
        },
      },
    });
    expect(mockLayerGroup).toHaveBeenCalledTimes(1);
    expect(mockCircle).toHaveBeenCalledWith(
      expect.objectContaining({
        center: {
          lat: 10,
          lng: 20,
        },
        radius: 20,
        color: colorFor(true, true),
        interactive: false,
      })
    );
  });
});
