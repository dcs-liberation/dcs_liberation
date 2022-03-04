// Based on https://thenable.io/building-a-use-socket-hook-in-react.
import { WEBSOCKET_URL } from "../../api/backend";
import { ReactChild, createContext, useEffect, useState } from "react";

const socket = new WebSocket(WEBSOCKET_URL);

export const SocketContext = createContext(socket);

interface SocketProviderProps {
  children: ReactChild;
}

export const SocketProvider = (props: SocketProviderProps) => {
  const [ws, setWs] = useState<WebSocket>(socket);
  useEffect(() => {
    const onClose = () => {
      setWs(new WebSocket(WEBSOCKET_URL));
    };

    const onError = (error: Event) => {
      console.log(`Websocket error: ${error}`);
    };

    ws.addEventListener("close", onClose);
    ws.addEventListener("error", onError);

    return () => {
      ws.removeEventListener("close", onClose);
      ws.removeEventListener("error", onError);
    };
  });

  return (
    <SocketContext.Provider value={ws}>{props.children}</SocketContext.Provider>
  );
};
