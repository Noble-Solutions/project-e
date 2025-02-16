import { baseApi } from "../../../shared/api/api";
import { clasroomWithStudentsAndTeacher } from "../../../shared/types/classrooms";
import { studentRead } from "../../../shared/types/user";

const singleClassroomApi = baseApi.injectEndpoints({
    endpoints: (build) => ({
        getClassroomByIdWithStudentsAndTeacher: build.query<clasroomWithStudentsAndTeacher, string | undefined>({
            query: (classroomId) => ({
                url: 'classrooms/get_classroom_by_id_with_students',
                method: 'GET',
                params: { classroom_id: classroomId }
            }),
            providesTags: ['Classrooms'],
            transformResponse: (response: {classroom: clasroomWithStudentsAndTeacher}) => response.classroom,
            
        }),
        getStudentByUsername: build.mutation<studentRead, string | undefined>({
            query: (username) => ({
                url: 'classrooms/find_student',
                method: 'GET',
                params: { student_name: username }
            }),
        }),
        addStudentToClassroom: build.mutation<void, {classroom_id: string, student_id: string}>({
            query: ({ classroom_id, student_id }) => ({
                url: 'classrooms/add_student',
                method: 'POST',
                params: { classroom_id, student_id }
            }),
            invalidatesTags: ['Classrooms']
        }),
        removeStudentFromClassroom: build.mutation<void, {classroom_id: string, student_id: string}>({
            query: ({ classroom_id, student_id }) => ({
                url: 'classrooms/delete_student',
                method: 'DELETE',
                params: { classroom_id, student_id }
            }),
            invalidatesTags: ['Classrooms']
        })
    })
})

export const { 
    useGetClassroomByIdWithStudentsAndTeacherQuery, 
    useGetStudentByUsernameMutation, 
    useAddStudentToClassroomMutation,
    useRemoveStudentFromClassroomMutation
} = singleClassroomApi