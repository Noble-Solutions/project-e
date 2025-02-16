import { baseApi } from "../../../shared/api/api";
import { classroomRead} from "../../../shared/types/classrooms";

const variantsApi = baseApi.injectEndpoints({
    endpoints: (build) => ({
        createVariant: build.mutation<classroomRead, {name: string}>({
            query: (variant) => ({
                url: '/variants',
                method: 'POST',
                body: variant
            }),
            invalidatesTags: ['Variants']
        })
    })
})

export const { useCreateVariantMutation } = variantsApi