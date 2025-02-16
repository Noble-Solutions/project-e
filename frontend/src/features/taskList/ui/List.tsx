import { Link } from "react-router-dom"
import { useGetAllTasksOfTeacherQuery } from "../api/api"
import { TaskCard } from "../../../entities/task"
import BackendError from "../../../shared/ui/BackendError"
export const List = () => {
    const { 
        data: tasksListData, 
        isSuccess: isTasksListDataSuccess, 
        error: tasksListDataError, 
        isError: isTasksListDataError 
    } = useGetAllTasksOfTeacherQuery()
    return (
        // TODO отстилизовать кнопку создать задание
        <div>
            <Link
            to="../create" 
            relative="path"
            >
                Создать задание
            </Link>
            <div className="flex justify-center w-full lg:w-[84%] lg:mx-auto mt-6 pb-6">
            {isTasksListDataError && <BackendError error={tasksListDataError}/>}
            {isTasksListDataSuccess &&
                <div className="flex flex-col gap-4">
                    <div className="grid lg:grid-cols-3 md:grid-cols-2 grid-cols-1 gap-x-10 gap-y-10 ">
                        {
                        isTasksListDataSuccess &&
                        tasksListData.map((task) => <TaskCard key={task.id} {...task}/>)
                        }
                    </div>
                </div>
            }
            </div>
        </div>
    )
}