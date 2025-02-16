import { baseApi } from "../../../shared/api/api";
import { classroomRead} from "../../../shared/types/classrooms";

const classroomsApi = baseApi.injectEndpoints({
    endpoints: (build) => ({
        createClassroom: build.mutation<classroomRead, {name: string}>({
            query: (classroom) => ({
                url: '/classrooms/create_classroom',
                method: 'POST',
                body: classroom
            }),
            invalidatesTags: ['Classrooms']
        })
    })
})

export const { useCreateClassroomMutation } = classroomsApi