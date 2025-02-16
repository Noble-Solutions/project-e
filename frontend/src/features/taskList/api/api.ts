import { TaskRead } from "../../../entities/task";
import { baseApi } from "../../../shared/api/api";

const taskListApi = baseApi.injectEndpoints({
    endpoints: (build) => ({
        getAllTasksOfTeacher: build.query<TaskRead[], void>({
            query: () => ({
                url: '/tasks/get_all_tasks_of_teacher',
                method: 'GET'
            }),
            transformResponse: (response: {tasks: TaskRead[]}) => response.tasks,
            providesTags: ['Tasks']
        }),
        
    })
})

export const { useGetAllTasksOfTeacherQuery } = taskListApi
