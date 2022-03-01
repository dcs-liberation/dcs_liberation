import "./App.css";

import { ControlPoint } from "./api/controlpoint";
import { Flight } from "./api/flight";
import { LatLng } from "leaflet";
import LiberationMap from "./components/liberationmap";
import axios from "axios";
import { registerFlight } from "./api/flightsSlice";
import { setControlPoints } from "./api/controlPointsSlice";
import { useAppDispatch } from "./app/hooks";
import { useEffect } from "react";

function App() {
  const mapCenter: LatLng = new LatLng(25.58, 54.9);

  const dispatch = useAppDispatch();

  useEffect(() => {
    axios
      .get("http://[::1]:5000/control-points")
      .catch((error) => console.log(`Error fetching control points: ${error}`))
      .then((response) => {
        if (response != null) {
          dispatch(setControlPoints(response.data as ControlPoint[]));
        }
      });
    axios
      .get("http://[::1]:5000/flights?with_waypoints=true")
      .catch((error) => console.log(`Error fetching flights: ${error}`))
      .then((response) => {
        if (response != null) {
          for (const flight of response.data) {
            dispatch(registerFlight(flight as Flight));
          }
        }
      });
  });

  console.log(`mapCenter=${mapCenter}`);
  return (
    <div className="App">
      <LiberationMap mapCenter={mapCenter} />
    </div>
  );
}

export default App;
