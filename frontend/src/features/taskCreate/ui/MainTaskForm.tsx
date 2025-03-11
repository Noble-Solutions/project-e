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
            className="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">
                    Создать Задание
            </button>
        </>

    )
}