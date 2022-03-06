import { AppDispatch } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import backend from "./backend";
import Game from "./game";

export default function reloadGameState(dispatch: AppDispatch) {
  backend
    .get("/game")
    .catch((error) => console.log(`Error fetching game state: ${error}`))
    .then((response) => {
      if (response == null || response.data == null) {
        dispatch(gameUnloaded());
        return;
      }
      dispatch(gameLoaded(response.data as Game));
    });
}
