import { FrontLine as FrontLineModel } from "../../api/liberationApi";
import { Polyline } from "react-leaflet";

interface FrontLineProps {
  front: FrontLineModel;
}

function FrontLine(props: FrontLineProps) {
  return (
    <Polyline positions={props.front.extents} weight={8} color={"#fe7d0a"} />
  );
}

export default FrontLine;
