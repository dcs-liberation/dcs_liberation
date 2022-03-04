import LiberationMap from "./components/liberationmap";
import useEventStream from "./hooks/useEventSteam";
import useInitialGameState from "./hooks/useInitialGameState";
import { LatLng } from "leaflet";

function App() {
  const mapCenter: LatLng = new LatLng(25.58, 54.9);

  useInitialGameState();
  useEventStream();

  return (
    <div className="App">
      <LiberationMap mapCenter={mapCenter} />
    </div>
  );
}

export default App;
