import Aircraft from "./Aircraft";
import { render } from "@testing-library/react";
import { Icon } from "leaflet";

const mockMarker = jest.fn();
jest.mock("react-leaflet", () => ({
  Marker: (props: any) => {
    mockMarker(props);
  },
}));

test("grounded aircraft do not render", async () => {
  const { container } = render(
    <Aircraft
      flight={{
        id: "",
        blue: true,
        position: undefined,
        sidc: "",
        waypoints: [],
      }}
    />
  );

  expect(container).toBeEmptyDOMElement();
});

test("in-flight aircraft render", async () => {
  render(
    <Aircraft
      flight={{
        id: "",
        blue: true,
        position: {
          lat: 10,
          lng: 20,
        },
        sidc: "foobar",
        waypoints: [],
      }}
    />
  );

  expect(mockMarker).toHaveBeenCalledWith(
    expect.objectContaining({
      position: {
        lat: 10,
        lng: 20,
      },
      icon: expect.any(Icon),
    })
  );
});
