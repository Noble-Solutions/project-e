import { createSlice, PayloadAction } from "@reduxjs/toolkit"

interface S3FormState {
    fileNameToGetPresignedUrlFor: string;
    additionalFileNameToGetPresignedUrlFor: string

}

const initialState: S3FormState = {
    fileNameToGetPresignedUrlFor: '',
    additionalFileNameToGetPresignedUrlFor: ''
};

export const s3FormSlice = createSlice({
    name: 's3Form',
    initialState,
    reducers: {
        setFileNameToGetPresignedUrlFor(state, action: PayloadAction<string>) {
            state.fileNameToGetPresignedUrlFor = action.payload
        },
        setAdditionalFileNameToGetPresignedUrlFor(state, action: PayloadAction<string>) {
            state.additionalFileNameToGetPresignedUrlFor = action.payload
        },
    },
    selectors: {
        selectFileNameToGetPresignedUrlFor: (state) => state.fileNameToGetPresignedUrlFor,
        selectAdditionalFilenameToGetPresignedUrlFor: (state) => state.additionalFileNameToGetPresignedUrlFor
    }
})

export const { 
    setFileNameToGetPresignedUrlFor, 
    setAdditionalFileNameToGetPresignedUrlFor
} = s3FormSlice.actions

export const { 
    selectFileNameToGetPresignedUrlFor,
    selectAdditionalFilenameToGetPresignedUrlFor
} = s3FormSlice.selectors