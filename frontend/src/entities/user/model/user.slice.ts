import { PayloadAction, createSlice } from "@reduxjs/toolkit"
import { userRead } from "../../../shared/types/user"
import { FetchBaseQueryError } from "@reduxjs/toolkit/query"

type authState = {
    user: userRead | null
    token: string | null
    authError: FetchBaseQueryError | null
}

const authSlice = createSlice({
    name: 'auth',
    initialState: { 
        user: null,
        token: null,
        authError: null
    } as authState,
    reducers: {
        setUser: (state, action: PayloadAction<authState["user"]>) => {
            state.user = action.payload
        },
        setToken: (state, action: PayloadAction<authState["token"]>) => {
            state.token = action.payload
        },
        setAuthError: (state, action: PayloadAction<authState["authError"]>) => {
            state.authError = action.payload
        },
        logOut: (state) => {
            state.user = null
            state.token = null
        }
    },
    selectors: {
        selectCurrentUser: (state) => state.user,
        selectCurrentToken: (state) => state.token,
        selectAuthError: (state) => state.authError
    }
})

export const { setUser, setToken, setAuthError, logOut } = authSlice.actions
export const { selectCurrentUser, selectCurrentToken, selectAuthError } = authSlice.selectors

export default authSlice.reducer