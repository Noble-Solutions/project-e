import { TaskFormContainer } from "../../../shared/ui/TaskFormContainer"
import { MainTaskForm } from "./MainTaskForm"

export const TaskCreateForm = () => {
    return (
        <TaskFormContainer formElement={<MainTaskForm />} />
    )
}