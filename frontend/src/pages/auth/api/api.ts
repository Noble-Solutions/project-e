import { baseApi } from "../../../shared/api/api";
import { userRead, userCreate } from "../../../shared/types/user";
import { loginData } from "../types/auth.types";

const authApi = baseApi.injectEndpoints({
    endpoints: (create) => ({
        register: create.mutation<userRead, userCreate>({
            query(user) {
                return {
                    url: '/auth/register',
                    method: 'POST',
                    body: user,
                }
            },
        }),
        login: create.mutation<loginData, URLSearchParams>({
            query(loginData) {
                return {
                    url: '/auth/login',
                    method: 'POST',
                    body: loginData,
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                }
            },
        }),
        logout: create.mutation<void, void>({
            query: () => {
                return {
                    url: '/auth/logout',
                    method: 'POST',
                }
            },
        }),
        getUserInfo: create.query<userRead, void>({
            query: () => 'auth/me',
        }),
        refreshToken: create.mutation<loginData, void>({
            query: () => {
                return {
                    url: '/auth/refresh',
                    method: 'POST',
                }
            },
        }),
    }),
    overrideExisting: true,
})

export const {
    useRegisterMutation,
    useLoginMutation,
    useLogoutMutation,
    useLazyGetUserInfoQuery,
    useRefreshTokenMutation,
} = authApi