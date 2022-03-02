import { ControlPoint } from "../api/controlpoint";
import { Flight } from "../api/flight";
import Tgo from "../api/tgo";
import backend from "../api/backend";
import { registerFlight } from "../api/flightsSlice";
import { setControlPoints } from "../api/controlPointsSlice";
import { setTgos } from "../api/tgosSlice";
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
      .get("/tgos")
      .catch((error) => console.log(`Error fetching TGOs: ${error}`))
      .then((response) => {
        if (response != null) {
          dispatch(setTgos(response.data as Tgo[]));
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
