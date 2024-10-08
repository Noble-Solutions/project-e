import { baseApi } from "../../../shared/api/api";
import { classroomListFromDB } from "../../../shared/types/classrooms";

const classroomsApi = baseApi.injectEndpoints({
    endpoints: (build) => ({
        getAllClassroomsOfUser: build.query<classroomListFromDB, void>({
            query: () => ({
                url: '/classrooms/get_all_classrooms_of_user',
                method: 'GET'
            })
        })
    })
})

export const { useGetAllClassroomsOfUserQuery } = classroomsApi