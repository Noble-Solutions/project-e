import { memo } from "react";
import { FetchBaseQueryError } from "@reduxjs/toolkit/query";
import { SerializedError } from "@reduxjs/toolkit";
import { errorData } from "../types/error";



const BackendError = memo(({ error }: {error: FetchBaseQueryError | SerializedError}) => {
    console.log(error)
      if ('data' in error) {
        return <>Error: {JSON.stringify((error.data as errorData).detail)} <br /> Status: {error.status}</>;
    }
})

export default BackendError