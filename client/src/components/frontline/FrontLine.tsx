import {
  FrontLine as FrontLineModel,
  useOpenNewFrontLinePackageDialogMutation,
} from "../../api/liberationApi";
import { Polyline } from "react-leaflet";

interface FrontLineProps {
  front: FrontLineModel;
}

function FrontLine(props: FrontLineProps) {
  const [openNewPackageDialog] = useOpenNewFrontLinePackageDialogMutation();
  return (
    <Polyline
      positions={props.front.extents}
      weight={16}
      color={"#fe7d0a"}
      eventHandlers={{
        contextmenu: () => {
          openNewPackageDialog({ frontLineId: props.front.id });
        },
      }}
    />
  );
}

export default FrontLine;
