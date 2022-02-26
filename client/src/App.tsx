import { LatLng } from "leaflet";
import "./App.css";

import { LiberationMap } from "./map/liberationmap/LiberationMap";
import { ControlPoint } from "./game/controlpoint";
import { useEffect } from "react";
import { useAppDispatch } from "./app/hooks";
import { setControlPoints } from "./game/theater/theaterSlice";
import axios from "axios";

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
  });

  console.log(`mapCenter=${mapCenter}`);
  return (
    <div className="App">
      <LiberationMap mapCenter={mapCenter} />
    </div>
  );
}

export default App;
