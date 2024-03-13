import { Game } from "./liberationApi";
import { createAction } from "@reduxjs/toolkit";

export const gameLoaded = createAction<Game>("game/loaded");
export const gameUnloaded = createAction("game/unloaded");
