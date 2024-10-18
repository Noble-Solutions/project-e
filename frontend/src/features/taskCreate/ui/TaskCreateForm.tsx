import { TaskFormContainer } from "../../../entities/task"
import { MainTaskForm } from "./MainTaskForm"

export const TaskCreateForm = () => {
    return (
        <TaskFormContainer formElement={<MainTaskForm />} />
    )
}