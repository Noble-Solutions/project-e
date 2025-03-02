import { baseApi } from "../../../shared/api/api";
import { checkVariantResponse, getVariantByIdWithTasksResponse } from "./types";

const singleVariantApi = baseApi.injectEndpoints({
    endpoints: (build) => ({
        getVariantByIdWithTasks: build.query<getVariantByIdWithTasksResponse, string | undefined>({
            query: (variantId) => ({
                url: `variants/${variantId}/`,
                method: 'GET',
            }),
            providesTags: ['Variants'],
            transformResponse: (response: {variant: getVariantByIdWithTasksResponse}) => response.variant,
        }),
        checkVariant: build.mutation<checkVariantResponse, {variant_id: string, classroom_id: string, answers: {[key: string]: string }}>({
            query: ({variant_id, classroom_id, answers}) => ({
                url: `variants/check/${variant_id}`,
                params: { classroom_id },
                method: 'POST',
                body: answers
            })
        })
    })
})

export const { 
    useGetVariantByIdWithTasksQuery,
    useCheckVariantMutation
} = singleVariantApi