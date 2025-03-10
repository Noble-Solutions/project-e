import { TaskFormFields } from "../../../entities/task"
import { S3SubmitForm } from "./s3SubmitForm"
import { useMainTaskFormHandleSubmit } from "../utils/formHandlers"
import { useEffect, useRef } from "react"
import { selectFormData } from "../../../entities/task"
import { useAppSelector } from "../../../shared/store"
import { manualFormSubmitTrigger } from "../../../shared/utils/utils"
import { useParams } from "react-router-dom"

export const MainTaskForm = () => {
    const formRef = useRef<HTMLFormElement>(null);
    const { handleSubmit } = useMainTaskFormHandleSubmit()
    const formData = useAppSelector(selectFormData)
    
    const { variant_id } = useParams()
    useEffect(() => {
        console.log(variant_id)
    })
    return (
        <>
            <form 
            ref={formRef}
            onSubmit={() => handleSubmit(formData, variant_id || null)}
            >
                <TaskFormFields />
            </form>
            <S3SubmitForm />
            <button
            onClick={() => manualFormSubmitTrigger(formRef)} 
            type="button" 
            className="inline-flex items-center px-5 py-2.5 mt-4 sm:mt-6 text-sm font-medium text-center text-white bg-primary-700 rounded-lg focus:ring-4 focus:ring-primary-200 dark:focus:ring-primary-900 hover:bg-primary-800">
                    Создать задание
            </button>
        </>

    )
}