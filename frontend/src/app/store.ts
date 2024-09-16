import { configureStore } from "@reduxjs/toolkit";
import { baseApi } from "../shared/api/api"
import { useDispatch, useSelector, useStore } from "react-redux";
export const store = configureStore({
    reducer: {
        [baseApi.reducerPath]: baseApi.reducer,
    },
    devTools: true,
    middleware: getDefaultMiddleware => getDefaultMiddleware().concat(baseApi.middleware)
})

export type AppDispatch = typeof store.dispatch;
export type AppState = ReturnType<typeof store.getState>;

export const useAppSelector = useSelector.withTypes<AppState>();
export const useAppDispatсh = useDispatch.withTypes<AppDispatch>();
export const useAppStore = useStore.withTypes<typeof store>();