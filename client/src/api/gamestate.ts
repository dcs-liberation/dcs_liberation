import { AppDispatch } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import backend from "./backend";
import { Game } from "./liberationApi";

export default function reloadGameState(
  dispatch: AppDispatch,
  ignoreRecenter: boolean = false
) {
  backend
    .get("/game")
    .catch((error) => console.log(`Error fetching game state: ${error}`))
    .then((response) => {
      if (response == null || response.data == null) {
        dispatch(gameUnloaded());
        return;
      }
      const game = response.data as Game;
      if (ignoreRecenter) {
        game.map_center = undefined;
      }
      dispatch(gameLoaded(game));
    });
}
