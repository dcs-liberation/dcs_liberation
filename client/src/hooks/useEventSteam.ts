import { useCallback, useEffect } from "react";

import { handleStreamedEvents } from "../api/eventstream";
import { useAppDispatch } from "../app/hooks";
import { useSocket } from "./useSocket";

export const useEventStream = () => {
  const ws = useSocket();
  const dispatch = useAppDispatch();

  const onMessage = useCallback(
    (message) => {
      handleStreamedEvents(dispatch, JSON.parse(message.data));
    },
    [dispatch]
  );

  useEffect(() => {
    ws.addEventListener("message", onMessage);
    return () => {
      ws.removeEventListener("message", onMessage);
    };
  });
};

export default useEventStream;
