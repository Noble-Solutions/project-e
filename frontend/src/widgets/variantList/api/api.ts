import { baseApi } from "../../../shared/api/api";

const variantsApi = baseApi.injectEndpoints({
    endpoints: (build) => ({
        getVariants: build.query({
            query: () => ({
                url: '/variants',
                method: 'GET'
            })
        })
    })
})

export const { useGetVariantsQuery } = variantsApi