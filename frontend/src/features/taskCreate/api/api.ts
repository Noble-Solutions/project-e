import { baseApi } from "../../../shared/api/api";
import { taskCreateQueryResponse, taskCreateQueryBody } from "./types";




const taskCreateApi = baseApi.injectEndpoints({
    endpoints: (build) => ({
        createTask: 
        build.mutation<taskCreateQueryResponse, taskCreateQueryBody>({
            query: (arg) => ({
                url: 'tasks/create_task',
                method: 'POST',
                body: arg
            })
        })
    })
})

export const { useCreateTaskMutation } = taskCreateApi