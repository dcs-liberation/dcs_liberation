import reloadGameState from "../api/gamestate";
import { useAppDispatch } from "../app/hooks";
import { useEffect } from "react";

// TODO: This should probably be distinct useControlPoints, useFlights, etc that
// are smart enough to only initialize once which get called in the components
// that use them rather than forcibly loading the whole game in the root
// component.
export const useInitialGameState = () => {
  const dispatch = useAppDispatch();
  useEffect(() => {
    reloadGameState(dispatch);
  });
};

export default useInitialGameState;
