import { baseApi } from "../../../shared/api/api";
import { VariantRead } from "./types";

const classroomsApi = baseApi.injectEndpoints({
    endpoints: (build) => ({
        getAllVariantsOfUser: build.query<VariantRead[], void>({
            query: () => ({
                url: 'variants/',
                method: 'GET'
            }),
            providesTags: ['Variants'],
            transformResponse: (response: {variants: VariantRead[]}) => response.variants
        }),
        // TODO: добавить classroom_id в этот реквест тоже
        assignVariantToStudent: build.mutation<void, {variant_id: string, student_id: string}>({
            query: ({variant_id, student_id}) => ({
                url: `variants/assign_variant_to_student/${variant_id}/${student_id}`,
                method: 'POST',
            }),
            invalidatesTags: ['Classrooms']
        }),
        assignVariantToClassroom: build.mutation<void, {variant_id: string, classroom_id: string}>({
            query: ({variant_id, classroom_id}) => ({
                url: `variants/assign_to_classroom/${variant_id}/${classroom_id}`,
                method: 'POST',
            }),
            invalidatesTags: ['Classrooms']
        }),
        deleteVariant: build.mutation<void, {variant_id: string}>({
            query: ({variant_id}) => ({
                url: `variants/${variant_id}`,
                method: 'DELETE',
            }),
            invalidatesTags: ['Variants']
        })
    })
})

export const { 
    useGetAllVariantsOfUserQuery, 
    useAssignVariantToStudentMutation, 
    useAssignVariantToClassroomMutation, 
    useDeleteVariantMutation
} = classroomsApi