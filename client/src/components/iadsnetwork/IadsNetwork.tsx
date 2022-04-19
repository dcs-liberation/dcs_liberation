import { IadsConnection as IadsConnectionModel } from "../../api/liberationApi";
import { Polyline as LPolyline } from "leaflet";
import { useRef } from "react";
import { Polyline, Tooltip } from "react-leaflet";

interface IadsConnectionProps {
  iads_connection: IadsConnectionModel;
}

function IadsConnectionTooltip(props: IadsConnectionProps) {
  var status = props.iads_connection.active ? "Active" : "Inactive"; 
  if (props.iads_connection.is_power) {
    return <Tooltip>Power Connection ({status})</Tooltip>;
  } else {
    return <Tooltip>Communication Connection ({status})</Tooltip>;
  }
}


export default function IadsConnection(props: IadsConnectionProps) {
  const color = props.iads_connection.is_power ? "#FFD580" : "#87CEEB";
  const path = useRef<LPolyline | null>();
  const weight = 1
  var opacity = props.iads_connection.active ? 1.0 : 0.5
  var dashArray = props.iads_connection.active ? "" : "20"

  return (
    <Polyline
      positions={props.iads_connection.points}
      color={color}
      weight={weight}
      opacity={opacity}
      dashArray={dashArray}
      ref={(ref) => (path.current = ref)}
    >
      <IadsConnectionTooltip {...props} />
    </Polyline>
  );
}
