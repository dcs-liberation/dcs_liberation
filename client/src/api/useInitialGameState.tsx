import { ControlPoint } from "./controlpoint";
import { Flight } from "./flight";
import backend from "./backend";
import { registerFlight } from "./flightsSlice";
import { setControlPoints } from "./controlPointsSlice";
import { useAppDispatch } from "../app/hooks";
import { useEffect } from "react";

// TODO: This should probably be distinct useControlPoints, useFlights, etc that
// are smart enough to only initialize once which get called in the components
// that use them rather than forcibly loading the whole game in the root
// component.
export const useInitialGameState = () => {
  const dispatch = useAppDispatch();
  useEffect(() => {
    backend
      .get("/control-points")
      .catch((error) => console.log(`Error fetching control points: ${error}`))
      .then((response) => {
        if (response != null) {
          dispatch(setControlPoints(response.data as ControlPoint[]));
        }
      });
    backend
      .get("/flights?with_waypoints=true")
      .catch((error) => console.log(`Error fetching flights: ${error}`))
      .then((response) => {
        if (response != null) {
          for (const flight of response.data) {
            dispatch(registerFlight(flight as Flight));
          }
        }
      });
  });
};

export default useInitialGameState;
