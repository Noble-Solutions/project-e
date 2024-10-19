import { TaskRead } from "../../../entities/task";
import { baseApi } from "../../../shared/api/api";

const taskListApi = baseApi.injectEndpoints({
    endpoints: (build) => ({
        getAllTasksOfTeacher: build.query<TaskRead[], void>({
            query: () => ({
                url: '/tasks/get_all_tasks_of_teacher',
                method: 'GET'
            })
        }),
        getPresignedUrlForGetFromS3: build.query<string, string>({
            query: (arg) => ({
                url: `/tasks/get_presigned_url_for_get_from_s3`,
                method: 'GET',
                params: { full_file_name: arg }
            })
        })
    })
})

export const { useGetAllTasksOfTeacherQuery, useGetPresignedUrlForGetFromS3Query } = taskListApi
