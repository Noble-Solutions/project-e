import { TaskFormFields } from "../../../shared/ui/TaskFormFields"
import { S3SubmitForm } from "./s3SubmitForm"
import { useMainTaskFormHandleSubmit } from "../utils/formHandlers"
import { manualFormSubmitTrigger } from "../utils/formHandlers"
import { useRef } from "react"
export const MainTaskForm = () => {
    const formRef = useRef<HTMLFormElement>(null);
    const { handleSubmit } = useMainTaskFormHandleSubmit()
    return (
        <>
            <form 
            ref={formRef}
            onSubmit={handleSubmit}
            >
                <TaskFormFields />
            </form>
            <S3SubmitForm />
            <button
            onClick={() => manualFormSubmitTrigger(formRef)} 
            type="button" 
            className="inline-flex items-center px-5 py-2.5 mt-4 sm:mt-6 text-sm font-medium text-center text-white bg-primary-700 rounded-lg focus:ring-4 focus:ring-primary-200 dark:focus:ring-primary-900 hover:bg-primary-800">
                    Add product
            </button>
        </>

    )
}