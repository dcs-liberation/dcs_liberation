import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { IadsConnection} from "./_liberationApi";

interface IadsNetworkState {
  connections: {[key: string]: IadsConnection}
}

const initialState: IadsNetworkState = {
  connections: {},
};

export const IadsNetworkSlice = createSlice({
  name: "iadsNetwork",
  initialState,
  reducers: {
    updateIadsConnection: (state, action: PayloadAction<IadsConnection>) => {
      const connection = action.payload;
      state.connections[connection.id] = connection
    },
  },
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      state.connections = action.payload.iads_network.connections.reduce(
        (acc: { [key: string]: IadsConnection }, curr) => {
          acc[curr.id] = curr;
          return acc;
        },
        {}
      );
    });
    builder.addCase(gameUnloaded, (state) => {
      state.connections = {};
    });
  },
});

export const { updateIadsConnection } = IadsNetworkSlice.actions;

export const selectIadsNetwork = (state: RootState) => state.iadsNetwork;

export default IadsNetworkSlice.reducer;
