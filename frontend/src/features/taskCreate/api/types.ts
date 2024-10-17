import { TaskCreate, TaskRead } from "../../../entities/task/types/types"

type s3SubmitFormProps = {
    "key": string,
    "x-amz-credential": string,
    "x-amz-algorithm": string,
    "x-amz-date": string,
    "policy": string,
    "x-amz-signature": string,
}

export type taskCreateQueryBody = {
    task_create: TaskCreate,
    file_extension?: string
}

export type taskCreateQueryResponse = {
    task: TaskRead,
    presigned_url_data_object: {
        url: string,
        fields: s3SubmitFormProps
    }
}