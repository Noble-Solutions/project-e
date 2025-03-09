import { createApi, fetchBaseQuery, BaseQueryFn, FetchArgs, FetchBaseQueryError } from '@reduxjs/toolkit/query/react'


/* 
ФИКС ЕСЛИ НЕ ТИПИЗИРУЮТСЯ АВТОМАТИЧЕСКИ СГЕНЕРИРОВАННЫЕ ХУКИ RTK QUERY
*/
// import * as _rtkQueryBuildHooksTypes from "../../../node_modules/@reduxjs/toolkit/dist/query/react/buildHooks"

// Если вы хотите получить API_URL из переменных окружения
// const API_URL : string = import.meta.env.VITE_API_URL

const API_URL : string = 'http://localhost:8000/api'

const baseQuery = fetchBaseQuery({
  baseUrl: API_URL,
  credentials: 'include', // Включаем передачу cookies
})

const baseQueryWithReauth: BaseQueryFn<string | FetchArgs, unknown, FetchBaseQueryError> = async (
  args,
  api,
  extraOptions
) => {
  let result = await baseQuery(args, api, extraOptions)

  // Если запрос вернул 401 Unauthorized, обновляем токен
  if (result.error && result.error.status === 401) {
      const refreshResult = await baseQuery(
          { url: '/auth/refresh', method: 'POST' },
          api,
          extraOptions
      )

      if (refreshResult.data) {
          // Повторяем исходный запрос с новым токеном
          result = await baseQuery(args, api, extraOptions)
      } else {
          // Если обновление токена не удалось, выходим
          // Например, можно вызвать logout
      }
  }

  return result
}

export const baseApi = createApi({
  baseQuery: baseQueryWithReauth,
  tagTypes: ['Classrooms', 'Tasks', 'Variants'],
  endpoints: () => ({}),
})