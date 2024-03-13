import { ControlPoint as ControlPointModel } from "../../api/liberationApi";
import { MobileControlPoint } from "./MobileControlPoint";
import { StaticControlPoint } from "./StaticControlPoint";

interface ControlPointProps {
  controlPoint: ControlPointModel;
}

export default function ControlPoint(props: ControlPointProps) {
  if (props.controlPoint.mobile) {
    return <MobileControlPoint {...props} />;
  } else {
    return <StaticControlPoint {...props} />;
  }
}
