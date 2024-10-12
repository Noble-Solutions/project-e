import { baseApi } from "../../../shared/api/api";

type s3SubmitFormProps = {
    "key": string,
    "bucket_name": string,
    "X-Amz-Credential": string,
    "acl": string,
    "X-Amz-Algorithm": string,
    "X-Amz-Date": string,
    "success_action_redirect": string,
    "policy": string,
    "X-Amz-Signature": string,
}

const taskCreateApi = baseApi.injectEndpoints({
    endpoints: (build) => ({
        getPresignedUrlForUploadToS3: build.query<s3SubmitFormProps, string>({
            query: (full_file_name) => ({
                url: 'tasks/get_presigned_url_for_upload_to_s3',
                method: 'GET',
                params: { full_file_name }
            })
        })
    })
})

export const { useLazyGetPresignedUrlForUploadToS3Query } = taskCreateApi