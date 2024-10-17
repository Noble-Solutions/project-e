import { TaskFormContainer } from "../../../entities/task/ui/TaskFormContainer"
import { MainTaskForm } from "./MainTaskForm"

export const TaskCreateForm = () => {
    return (
        <TaskFormContainer formElement={<MainTaskForm />} />
    )
}