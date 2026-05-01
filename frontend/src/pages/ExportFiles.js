import { lazy } from "react";
const HomePage = lazy(() => import("./HomePage"));
const CreateRoomForm = lazy(() => import("./CreateRoomFormPage"));
const JoinRoomForm = lazy(() => import("./JoinRoomFormPage"));

export { HomePage, CreateRoomForm, JoinRoomForm };
