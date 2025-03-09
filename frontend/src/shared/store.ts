import { configureStore, combineReducers } from "@reduxjs/toolkit";
import { baseApi } from "./api/api";
import { authSlice } from "../entities/user/model/user.slice";
import { s3FormSlice } from "../features/taskCreate/model/slice";
import { taskFormFieldsSlice } from "../entities/task";
import { variantAnswersSlice } from "../features/singleVariant/model/slice";
import { useDispatch, useSelector, useStore } from "react-redux";

// Импортируем redux-persist
import { persistStore, persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage"; // Используем localStorage

// Конфигурация для redux-persist
const persistConfig = {
    key: "root", // Ключ для хранения в localStorage
    storage, // Используем localStorage
    whitelist: [authSlice.reducerPath], // Сохраняем только данные из authSlice
    blacklist: [baseApi.reducerPath], // Исключаем кеш RTK Query
};

// Объединяем редьюсеры
const rootReducer = combineReducers({
    [baseApi.reducerPath]: baseApi.reducer,
    [authSlice.reducerPath]: authSlice.reducer,
    [s3FormSlice.reducerPath]: s3FormSlice.reducer,
    [taskFormFieldsSlice.reducerPath]: taskFormFieldsSlice.reducer,
    [variantAnswersSlice.reducerPath]: variantAnswersSlice.reducer,
});

// Применяем persistReducer к корневому редьюсеру
const persistedReducer = persistReducer(persistConfig, rootReducer);

// Создаем store с persistedReducer
export const store = configureStore({
    reducer: persistedReducer,
    devTools: true,
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: {
                ignoredActions: ["persist/PERSIST"], // Игнорируем действия redux-persist
            },
        }).concat(baseApi.middleware), // Подключаем middleware RTK Query
});

// Создаем persistor для работы с redux-persist
export const persistor = persistStore(store);

// Типы для TypeScript
export type AppDispatch = typeof store.dispatch;
export type AppState = ReturnType<typeof store.getState>;

// Типизированные хуки
export const useAppSelector = useSelector.withTypes<AppState>();
export const useAppDispatсh = useDispatch.withTypes<AppDispatch>();
export const useAppStore = useStore.withTypes<typeof store>();