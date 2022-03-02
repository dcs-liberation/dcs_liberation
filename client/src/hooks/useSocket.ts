import { SocketContext } from "../components/socketprovider/socketprovider";
import { useContext } from "react";

export const useSocket = () => {
  const socket = useContext(SocketContext);

  return socket;
};
