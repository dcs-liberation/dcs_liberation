import backend from "../../api/backend";
import { ControlPoint as ControlPointModel } from "../../api/controlpoint";
import {
  useClearControlPointDestinationMutation,
  useSetControlPointDestinationMutation,
} from "../../api/liberationApi";
import {
  Icon,
  LatLng,
  Point,
  Marker as LMarker,
  Polyline as LPolyline,
} from "leaflet";
import { Symbol as MilSymbol } from "milsymbol";
import {
  MutableRefObject,
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";
import ReactDOMServer from "react-dom/server";
import { Marker, Polyline, Tooltip } from "react-leaflet";

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

function openInfoDialog(controlPoint: ControlPointModel) {
  backend.post(`/qt/info/control-point/${controlPoint.id}`);
}

function openNewPackageDialog(controlPoint: ControlPointModel) {
  backend.post(`/qt/create-package/control-point/${controlPoint.id}`);
}

interface ControlPointProps {
  controlPoint: ControlPointModel;
}

function LocationTooltipText(props: ControlPointProps) {
  return <h3 style={{ margin: 0 }}>{props.controlPoint.name}</h3>;
}

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
  cp: ControlPointModel,
  destinationish: LatLng,
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

function PrimaryMarker(props: ControlPointProps) {
  // We can't use normal state to update the marker tooltip or the line points
  // because if we set any state in the drag event it will re-render the
  // component and interrupt dragging. Instead, keep refs to the objects and
  // mutate them directly.
  //
  // For the same reason, the path is owned by this component, because updating
  // sibling state would be messy. Lifting the state into the parent would still
  // cause this component to redraw.
  const marker: MutableRefObject<LMarker | undefined> = useRef();
  const pathLine: MutableRefObject<LPolyline | undefined> = useRef();

  const [hasDestination, setHasDestination] = useState<boolean>(
    props.controlPoint.destination != null
  );
  const [pathDestination, setPathDestination] = useState<LatLng>(
    props.controlPoint.destination
      ? props.controlPoint.destination
      : props.controlPoint.position
  );
  const [position, setPosition] = useState<LatLng>(
    props.controlPoint.destination
      ? props.controlPoint.destination
      : props.controlPoint.position
  );

  const setDestination = useCallback((destination: LatLng) => {
    setPathDestination(destination);
    setPosition(destination);
    setHasDestination(true);
  }, []);

  const resetDestination = useCallback(() => {
    setPathDestination(props.controlPoint.position);
    setPosition(props.controlPoint.position);
    setHasDestination(false);
  }, [props.controlPoint.position]);

  const [putDestination, { isLoading }] =
    useSetControlPointDestinationMutation();
  const [cancelTravel] = useClearControlPointDestinationMutation();

  useEffect(() => {
    marker.current?.setTooltipContent(
      props.controlPoint.destination
        ? destinationTooltipText(
            props.controlPoint,
            props.controlPoint.destination,
            true
          )
        : ReactDOMServer.renderToString(
            <LocationTooltipText controlPoint={props.controlPoint} />
          )
    );
  });

  return (
    <>
      <Marker
        position={position}
        icon={iconForControlPoint(props.controlPoint)}
        draggable={props.controlPoint.mobile && !isLoading}
        autoPan
        // We might draw other markers on top of the CP. The tooltips from the
        // other markers are helpful so we want to keep them, but make sure the CP
        // is always the clickable thing.
        zIndexOffset={1000}
        opacity={props.controlPoint.destination ? 0.5 : 1}
        ref={(ref) => {
          if (ref != null) {
            marker.current = ref;
          }
        }}
        eventHandlers={{
          click: () => {
            if (!hasDestination) {
              openInfoDialog(props.controlPoint);
            }
          },
          contextmenu: () => {
            if (props.controlPoint.destination) {
              cancelTravel({ cpId: props.controlPoint.id }).then(() => {
                resetDestination();
              });
            } else {
              openNewPackageDialog(props.controlPoint);
            }
          },
          drag: (event) => {
            const destination = event.target.getLatLng();
            backend
              .get(
                `/control-points/${props.controlPoint.id}/destination-in-range?lat=${destination.lat}&lng=${destination.lng}`
              )
              .then((inRange) => {
                marker.current?.setTooltipContent(
                  destinationTooltipText(
                    props.controlPoint,
                    destination,
                    inRange.data
                  )
                );
              });
            pathLine.current?.setLatLngs([
              props.controlPoint.position,
              destination,
            ]);
          },
          dragend: async (event) => {
            const currentPosition = new LatLng(
              pathDestination.lat,
              pathDestination.lng,
              pathDestination.alt
            );
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
      <Polyline
        positions={[props.controlPoint.position, pathDestination]}
        weight={1}
        color="#80BA80"
        interactive
        ref={(ref) => {
          if (ref != null) {
            pathLine.current = ref;
          }
        }}
      />
    </>
  );
}

interface SecondaryMarkerProps {
  controlPoint: ControlPointModel;
  destination: LatLng | null;
}

function SecondaryMarker(props: SecondaryMarkerProps) {
  if (!props.destination) {
    return <></>;
  }

  return (
    <Marker
      position={props.controlPoint.position}
      icon={iconForControlPoint(props.controlPoint)}
      // We might draw other markers on top of the CP. The tooltips from the
      // other markers are helpful so we want to keep them, but make sure the CP
      // is always the clickable thing.
      zIndexOffset={1000}
      eventHandlers={{
        click: () => {
          openInfoDialog(props.controlPoint);
        },
        contextmenu: () => {
          openNewPackageDialog(props.controlPoint);
        },
      }}
    >
      <Tooltip>
        <LocationTooltipText {...props} />
      </Tooltip>
    </Marker>
  );
}

export default function ControlPoint(props: ControlPointProps) {
  return (
    <>
      <PrimaryMarker {...props} />
      <SecondaryMarker
        controlPoint={props.controlPoint}
        destination={props.controlPoint.destination}
      />
    </>
  );
}
