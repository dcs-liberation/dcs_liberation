import "./App.css";

import { LatLng } from "leaflet";
import LiberationMap from "./components/liberationmap";
import useInitialGameState from "./api/useInitialGameState";

function App() {
  const mapCenter: LatLng = new LatLng(25.58, 54.9);

  useInitialGameState();

  return (
    <div className="App">
      <LiberationMap mapCenter={mapCenter} />
    </div>
  );
}

export default App;
