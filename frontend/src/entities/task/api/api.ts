import { baseApi } from "../../../shared/api/api";

const taskApi = baseApi.injectEndpoints({
    endpoints: (build) => ({   
        getPresignedUrlForGetFromS3: build.query<string, string>({
            query: (arg) => ({
                url: `/tasks/get_presigned_url_for_get_from_s3`,
                method: 'GET',
                params: { full_file_name: arg }
            }),
            
        }),
        deleteTask: build.mutation<void, {task_id: string}>({
            query: ({task_id}) => ({
                url: `/tasks/${task_id}/`,
                method: 'DELETE',
            }),
            invalidatesTags: ['Tasks']
        })
    })
})

export const { useGetPresignedUrlForGetFromS3Query, useDeleteTaskMutation } = taskApi