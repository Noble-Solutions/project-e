import { FormEvent, RefObject } from "react";
import {  useLazyCreateTaskQuery } from "../api/api";
import { selectFileNameToGetPresignedUrlFor } from "../model/slice";
import { useAppSelector } from "../../../shared/store";

export const handleSubmitS3FileForm = async (event: FormEvent<HTMLFormElement>) => {
    return
}

export const manualFormSubmitTrigger =  (formRef: RefObject<HTMLFormElement>) => {
    if (formRef.current) {
        formRef.current.dispatchEvent(new Event('submit', { bubbles: true }));
    }
}

export const useMainTaskFormHandleSubmit = () => {
    const [getPresignedUrlForUploadToS3QueryTrigger] = useLazyCreateTaskQuery()
    const fileNameToPassInGetPresignedUrlForUploadToS3Query = useAppSelector(selectFileNameToGetPresignedUrlFor)
    const handleSubmit = async () => {
        try {
            const result = await getPresignedUrlForUploadToS3QueryTrigger(fileNameToPassInGetPresignedUrlForUploadToS3Query)
            console.log(result)
        } catch (err) {
            console.log(err)
        }
    }
    return { handleSubmit }
}

