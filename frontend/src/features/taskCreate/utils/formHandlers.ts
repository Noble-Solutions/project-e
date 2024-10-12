import { FormEvent, RefObject } from "react";
import { useLazyGetPresignedUrlForUploadToS3Query } from "../api/api";
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
    const [getPresignedUrlForUploadToS3QueryTrigger] = useLazyGetPresignedUrlForUploadToS3Query()
    const fileNameToPassInGetPresignedUrlForUploadToS3Query = useAppSelector(selectFileNameToGetPresignedUrlFor)
    const handleSubmit = async () => {
        try {
            await getPresignedUrlForUploadToS3QueryTrigger(fileNameToPassInGetPresignedUrlForUploadToS3Query)
        } catch (err) {
            console.log(err)
        }
    }
    return { handleSubmit }
}

