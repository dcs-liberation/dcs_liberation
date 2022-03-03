import { Icon, Point } from "leaflet";
import { Marker, Tooltip } from "react-leaflet";

import { ControlPoint as ControlPointModel } from "../../api/controlpoint";
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

export default function ControlPoint(props: ControlPointProps) {
  return (
    <Marker
      position={props.controlPoint.position}
      icon={iconForControlPoint(props.controlPoint)}
      // We might draw other markers on top of the CP. The tooltips from the
      // other markers are helpful so we want to keep them, but make sure the CP
      // is always the clickable thing.
      zIndexOffset={1000}
    >
      <Tooltip>
        <h3 style={{ margin: 0 }}>{props.controlPoint.name}</h3>
      </Tooltip>
    </Marker>
  );
}
