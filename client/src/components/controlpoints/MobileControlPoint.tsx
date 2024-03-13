import { ControlPoint } from "../../api/_liberationApi";
import backend from "../../api/backend";
import {
  useClearControlPointDestinationMutation,
  useSetControlPointDestinationMutation,
} from "../../api/liberationApi";
import { makeLocationMarkerEventHandlers } from "./EventHandlers";
import { iconForControlPoint } from "./Icons";
import LocationTooltipText from "./LocationTooltipText";
import { MovementPath, MovementPathHandle } from "./MovementPath";
import { StaticControlPoint } from "./StaticControlPoint";
import { LatLng, Marker as LMarker, LatLngLiteral } from "leaflet";
import { useCallback, useEffect, useRef, useState } from "react";
import ReactDOMServer from "react-dom/server";
import { Marker, Tooltip } from "react-leaflet";

function metersToNauticalMiles(meters: number) {
  return meters * 0.000539957;
}

function formatLatLng(latLng: LatLng) {
  const lat = latLng.lat.toFixed(2);
  const lng = latLng.lng.toFixed(2);
  const ns = latLng.lat >= 0 ? "N" : "S";
  const ew = latLng.lng >= 0 ? "E" : "W";
  return `${lat}&deg;${ns} ${lng}&deg;${ew}`;
}

function destinationTooltipText(
  cp: ControlPoint,
  destinationish: LatLngLiteral,
  inRange: boolean
) {
  const destination = new LatLng(destinationish.lat, destinationish.lng);
  const distance = metersToNauticalMiles(
    destination.distanceTo(cp.position)
  ).toFixed(1);
  if (!inRange) {
    return `Out of range (${distance}nm away)`;
  }
  const dest = formatLatLng(destination);
  return `${cp.name} moving ${distance}nm to ${dest} next turn`;
}

interface PrimaryMarkerProps {
  controlPoint: ControlPoint;
}

/**
 * The primary control point marker. For non-mobile control points, this has
 * fairly simple behavior: it's a marker in a fixed location that can manage
 * units and can have missions planned against it.
 *
 * For mobile control points, this is a draggable marker. If the control point
 * has a destination (either because it was dragged after render, or because it
 * had a destination in the game that was loaded), the unit management and
 * mission planning behaviors are delegated to SecondaryMarker, and the primary
 * marker becomes only a destination marker. It can be dragged to change the
 * destination, and can be right clicked to cancel movement.
 */
function PrimaryMarker(props: PrimaryMarkerProps) {
  // We can't use normal state to update the marker tooltip or the line points
  // because if we set any state in the drag event it will re-render this
  // component and all children, interrupting dragging. Instead, keep refs to
  // the objects and mutate them directly.
  //
  // For the same reason, the path is owned by this component, because updating
  // sibling state would be messy. Lifting the state into the parent would still
  // cause this component to redraw.
  const markerRef = useRef<LMarker | null>(null);
  const pathRef = useRef<MovementPathHandle | null>(null);

  const [hasDestination, setHasDestination] = useState<boolean>(
    props.controlPoint.destination != null
  );
  const [position, setPosition] = useState<LatLngLiteral>(
    props.controlPoint.destination
      ? props.controlPoint.destination
      : props.controlPoint.position
  );

  const setDestination = useCallback((destination: LatLng) => {
    setPosition(destination);
    setHasDestination(true);
  }, []);

  const resetDestination = useCallback(() => {
    setPosition(props.controlPoint.position);
    setHasDestination(false);
  }, [props]);

  const [putDestination, { isLoading }] =
    useSetControlPointDestinationMutation();
  const [cancelTravel] = useClearControlPointDestinationMutation();

  useEffect(() => {
    markerRef.current?.setTooltipContent(
      props.controlPoint.destination
        ? destinationTooltipText(
            props.controlPoint,
            props.controlPoint.destination,
            true
          )
        : ReactDOMServer.renderToString(
            <LocationTooltipText name={props.controlPoint.name} />
          )
    );
  });

  const locationClickHandlers = makeLocationMarkerEventHandlers(
    props.controlPoint
  );

  return (
    <>
      <Marker
        position={position}
        icon={iconForControlPoint(props.controlPoint)}
        draggable={!isLoading}
        autoPan
        // We might draw other markers on top of the CP. The tooltips from the
        // other markers are helpful so we want to keep them, but make sure the CP
        // is always the clickable thing.
        zIndexOffset={1000}
        opacity={props.controlPoint.destination ? 0.5 : 1}
        ref={(ref) => {
          if (ref != null) {
            markerRef.current = ref;
          }
        }}
        eventHandlers={{
          click: () => {
            if (!hasDestination) {
              locationClickHandlers.click();
            }
          },
          contextmenu: () => {
            if (props.controlPoint.destination) {
              cancelTravel({ cpId: props.controlPoint.id }).then(() => {
                resetDestination();
              });
            } else {
              locationClickHandlers.contextmenu();
            }
          },
          drag: (event) => {
            const destination = event.target.getLatLng();
            backend
              .get(
                `/control-points/${props.controlPoint.id}/destination-in-range?lat=${destination.lat}&lng=${destination.lng}`
              )
              .then((inRange) => {
                markerRef.current?.setTooltipContent(
                  destinationTooltipText(
                    props.controlPoint,
                    destination,
                    inRange.data
                  )
                );
              });
            pathRef.current?.setDestination(destination);
          },
          dragend: async (event) => {
            const currentPosition = new LatLng(position.lat, position.lng);
            const destination = event.target.getLatLng();
            setDestination(destination);
            try {
              await putDestination({
                cpId: props.controlPoint.id,
                body: { lat: destination.lat, lng: destination.lng },
              }).unwrap();
            } catch (error) {
              console.error("setDestination failed", error);
              setDestination(currentPosition);
            }
          },
        }}
      >
        <Tooltip />
      </Marker>
      <MovementPath
        source={props.controlPoint.position}
        destination={position}
        ref={pathRef}
      />
    </>
  );
}

interface SecondaryMarkerProps {
  controlPoint: ControlPoint;
  destination: LatLngLiteral | undefined;
}

/**
 * The secondary marker for a control point. The secondary marker will only be
 * shown when the control point has a destination set. For mobile control
 * points, the primary marker is draggable, and the secondary marker will be
 * shown at the current location iff the control point has been dragged. The
 * secondary marker is also the marker that has the normal control point
 * interaction options (mission planning and unit management).
 */
function SecondaryMarker(props: SecondaryMarkerProps) {
  if (!props.destination) {
    return <></>;
  }

  return <StaticControlPoint controlPoint={props.controlPoint} />;
}

interface MobileControlPointProps {
  controlPoint: ControlPoint;
}

export const MobileControlPoint = (props: MobileControlPointProps) => {
  return (
    <>
      <PrimaryMarker
        controlPoint={props.controlPoint}
        key={props.controlPoint.destination ? 0 : 1}
      />
      <SecondaryMarker
        controlPoint={props.controlPoint}
        destination={props.controlPoint.destination}
      />
    </>
  );
};
