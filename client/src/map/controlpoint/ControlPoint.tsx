import { Icon, Point } from "leaflet";
import { Marker, Popup } from "react-leaflet";
import { ControlPoint as ControlPointModel } from "../../game/controlpoint";
import { Symbol as MilSymbol } from "milsymbol";

function iconForControlPoint(cp: ControlPointModel) {
  const symbol = new MilSymbol(cp.sidc, {
    size: 24,
    colorMode: "Dark",
  });

  return new Icon({
    iconUrl: symbol.toDataURL(),
    iconAnchor: new Point(symbol.getAnchor().x, symbol.getAnchor().y),
  });
}

interface ControlPointProps {
  controlPoint: ControlPointModel;
}

export function ControlPoint(props: ControlPointProps) {
  return (
    <Marker
      position={props.controlPoint.position}
      icon={iconForControlPoint(props.controlPoint)}
    >
      <Popup>{props.controlPoint.name}</Popup>
    </Marker>
  );
}
