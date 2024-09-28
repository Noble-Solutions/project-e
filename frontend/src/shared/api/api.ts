import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { AppState } from '../store'

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
        credentials: 'include',
        prepareHeaders: (headers, { getState }) => {
            // By default, if we have a token in the store, let's use that for authenticated requests
            const token = (getState() as AppState).auth.token
            if (token) {
              headers.set('authorization', `Bearer ${token}`)
            }
            return headers 
          }
        }),    
    tagTypes: [],
    endpoints: () => ({}),
})