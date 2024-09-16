import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { AppState } from '../../app/store'

/* 
ФИКС ЕСЛИ НЕ ТИПИЗИРУЮТСЯ АВТОМАТИЧЕСКИ СГЕНЕРИРОВАННЫЕ ХУКИ RTK QUERY
*/
// import * as _rtkQueryBuildHooksTypes from "../../../node_modules/@reduxjs/toolkit/dist/query/react/buildHooks"

// Если вы хотите получить API_URL из переменных окружения
// const API_URL : string = import.meta.env.VITE_API_URL

const API_URL : string = 'http://localhost:8000/api'

export const baseApi = createApi({
    baseQuery: fetchBaseQuery({ 
        baseUrl: API_URL,
    }),
    tagTypes: [],
    endpoints: () => ({}),
})