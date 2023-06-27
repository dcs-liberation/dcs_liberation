import { renderWithProviders } from "../../testutils";
import SupplyRoute, { RouteColor } from "./SupplyRoute";
import { screen } from "@testing-library/react";
import { PropsWithChildren } from "react";

const mockPolyline = jest.fn();
jest.mock("react-leaflet", () => ({
  Polyline: (props: PropsWithChildren<any>) => {
    mockPolyline(props);
    return <>{props.children}</>;
  },
  Tooltip: (props: PropsWithChildren<any>) => {
    return <p data-testid="tooltip">{props.children}</p>;
  },
}));

describe("SupplyRoute", () => {
  it("is red when inactive and owned by opfor", () => {
    renderWithProviders(
      <SupplyRoute
        route={{
          id: "",
          points: [],
          front_active: false,
          is_sea: false,
          blue: false,
          active_transports: [],
        }}
      />
    );
    expect(mockPolyline).toHaveBeenCalledWith(
      expect.objectContaining({
        color: RouteColor.Red,
      })
    );
  });

  it("is blue when inactive and owned by bluefor", () => {
    renderWithProviders(
      <SupplyRoute
        route={{
          id: "",
          points: [],
          front_active: false,
          is_sea: false,
          blue: true,
          active_transports: [],
        }}
      />
    );
    expect(mockPolyline).toHaveBeenCalledWith(
      expect.objectContaining({
        color: RouteColor.Blue,
      })
    );
  });

  it("is orange when contested", () => {
    renderWithProviders(
      <SupplyRoute
        route={{
          id: "",
          points: [],
          front_active: true,
          is_sea: false,
          blue: false,
          active_transports: [],
        }}
      />
    );
    expect(mockPolyline).toHaveBeenCalledWith(
      expect.objectContaining({
        color: RouteColor.Contested,
      })
    );
  });

  it("is highlighted when the route has active transports", () => {
    renderWithProviders(
      <SupplyRoute
        route={{
          id: "",
          points: [],
          front_active: false,
          is_sea: false,
          blue: false,
          active_transports: ["foo"],
        }}
      />
    );
    expect(mockPolyline).toHaveBeenCalledTimes(2);
    expect(mockPolyline).toHaveBeenCalledWith(
      expect.objectContaining({
        color: RouteColor.Highlight,
      })
    );
  });

  it("is drawn in the right place", () => {
    const points = [
      { lat: 0, lng: 0 },
      { lat: 1, lng: 1 },
    ];
    renderWithProviders(
      <SupplyRoute
        route={{
          id: "",
          points: points,
          front_active: false,
          is_sea: false,
          blue: false,
          active_transports: ["foo"],
        }}
      />
    );
    expect(mockPolyline).toHaveBeenCalledTimes(2);
    expect(mockPolyline).toHaveBeenCalledWith(
      expect.objectContaining({
        positions: points,
      })
    );
  });

  it("has a tooltip describing an inactive supply route", () => {
    renderWithProviders(
      <SupplyRoute
        route={{
          id: "",
          points: [],
          front_active: false,
          is_sea: false,
          blue: false,
          active_transports: [],
        }}
      />
    );

    const tooltip = screen.getByTestId("tooltip");
    expect(tooltip).toHaveTextContent("This supply route is inactive.");
  });

  it("has a tooltip describing active supply routes", () => {
    renderWithProviders(
      <SupplyRoute
        route={{
          id: "",
          points: [],
          front_active: false,
          is_sea: false,
          blue: false,
          active_transports: ["foo", "bar"],
        }}
      />
    );

    const tooltip = screen.getByTestId("tooltip");
    expect(tooltip).toContainHTML("foo<br />bar");
  });
});
