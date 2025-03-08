import { PayloadAction, createSlice } from "@reduxjs/toolkit"
import { userRead } from "../../../shared/types/user"
import { FetchBaseQueryError } from "@reduxjs/toolkit/query"

type authState = {
    user: userRead | null
    token: string | null
    authError: FetchBaseQueryError | null
}

export const authSlice = createSlice({
    name: 'auth',
    initialState: { 
        user: null,
        authError: null
    } as authState,
    reducers: {
        setUser: (state, action: PayloadAction<authState["user"]>) => {
            state.user = action.payload
        },
        setAuthError: (state, action: PayloadAction<authState["authError"]>) => {
            state.authError = action.payload
        },
        logOut: (state) => {
            state.user = null
        }
    },
    selectors: {
        selectCurrentUser: (state) => state.user,
        selectAuthError: (state) => state.authError
    }
})

export const { setUser, setAuthError, logOut } = authSlice.actions
export const { selectCurrentUser, selectAuthError } = authSlice.selectors
