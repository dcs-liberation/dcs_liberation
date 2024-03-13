import { LatLngLiteral, Polyline as LPolyline } from "leaflet";
import { forwardRef, useImperativeHandle, useRef } from "react";
import { Polyline } from "react-leaflet";

interface MovementPathProps {
  source: LatLngLiteral;
  destination: LatLngLiteral;
}

export interface MovementPathHandle {
  setDestination: (destination: LatLngLiteral) => void;
}

export const MovementPath = forwardRef<MovementPathHandle, MovementPathProps>(
  (props: MovementPathProps, ref) => {
    const lineRef = useRef<LPolyline | null>(null);
    useImperativeHandle(
      ref,
      () => ({
        setDestination: (destination: LatLngLiteral) => {
          lineRef.current?.setLatLngs([props.source, destination]);
        },
      }),
      [props]
    );
    return (
      <Polyline
        positions={[props.source, props.destination]}
        weight={1}
        color="#80BA80"
        ref={lineRef}
      />
    );
  }
);
