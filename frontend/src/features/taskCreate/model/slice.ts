import { createSlice, PayloadAction } from "@reduxjs/toolkit"

export const s3FormSlice = createSlice({
    name: 's3Form',
    initialState: {
        fileNameToGetPresignedUrlFor: '',
    } as {
        fileNameToGetPresignedUrlFor: string,
    },
    reducers: {
        setFileNameToGetPresignedUrlFor(state, action: PayloadAction<string>) {
            state.fileNameToGetPresignedUrlFor = action.payload
        },
    },
    selectors: {
        selectFileNameToGetPresignedUrlFor: (state) => state.fileNameToGetPresignedUrlFor,
    }
})

export const { 
    setFileNameToGetPresignedUrlFor, 
} = s3FormSlice.actions

export const { 
    selectFileNameToGetPresignedUrlFor, 
} = s3FormSlice.selectors