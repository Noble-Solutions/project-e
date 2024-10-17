import { createSlice, PayloadAction } from "@reduxjs/toolkit"
import { RefObject } from "react"

interface S3FormState {
    fileNameToGetPresignedUrlFor: string;

}

const initialState: S3FormState = {
    fileNameToGetPresignedUrlFor: '',
};

export const s3FormSlice = createSlice({
    name: 's3Form',
    initialState,
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