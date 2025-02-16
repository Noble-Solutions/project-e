import { baseApi } from "../../../shared/api/api";

const variantsApi = baseApi.injectEndpoints({
    endpoints: (build) => ({   
          addTaskToVariant: build.mutation<void, {variant_id: string, task_id: string}>({
            query: ({ variant_id, task_id }) => ({
                url: `variants/add_task/${variant_id}/task/${task_id}`,
                method: 'POST',
            }),
            invalidatesTags: ['Variants']
        }),
        removeTaskFromVariant: build.mutation<void, { variant_id: string; task_id: string }>({
          query: ({ variant_id, task_id }) => ({
            url: `/variants/remove_task/${variant_id}/task/${task_id}`,
            method: 'DELETE'
          }),
          invalidatesTags: ['Variants']
        }),
    })
})

export const { useAddTaskToVariantMutation, useRemoveTaskFromVariantMutation } = variantsApi