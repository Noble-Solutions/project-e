import { baseApi } from "../../../shared/api/api";

const taskListApi = baseApi.injectEndpoints({
    endpoints: (build) => ({
        getAllTasksOfTeacher: build.query({
            query: () => ({
                url: '/tasks/get_all_tasks_of_teacher',
                method: 'GET'
            })
        })
    })
})