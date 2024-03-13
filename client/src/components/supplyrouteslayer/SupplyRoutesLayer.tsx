import { selectSupplyRoutes } from "../../api/supplyRoutesSlice";
import { useAppSelector } from "../../app/hooks";
import SupplyRoute from "../supplyroute/SupplyRoute";
import { LayerGroup } from "react-leaflet";

export default function SupplyRoutesLayer() {
  const routes = useAppSelector(selectSupplyRoutes).routes;
  return (
    <LayerGroup>
      {routes.map((route) => {
        return <SupplyRoute key={route.id} route={route} />;
      })}
    </LayerGroup>
  );
}
