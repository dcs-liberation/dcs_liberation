import { ControlPoint } from "../../api/_liberationApi";
import backend from "../../api/backend";

function openInfoDialog(controlPoint: ControlPoint) {
  backend.post(`/qt/info/control-point/${controlPoint.id}`);
}

function openNewPackageDialog(controlPoint: ControlPoint) {
  backend.post(`/qt/create-package/control-point/${controlPoint.id}`);
}

export const makeLocationMarkerEventHandlers = (controlPoint: ControlPoint) => {
  return {
    click: () => {
      openInfoDialog(controlPoint);
    },

    contextmenu: () => {
      openNewPackageDialog(controlPoint);
    },
  };
};
