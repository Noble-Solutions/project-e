import { FormEvent } from "react";
import { useCreateTaskMutation } from "../api/api";
import { selectFileNameToGetPresignedUrlFor } from "../model/slice";
import { useAppDispatсh, useAppSelector } from "../../../shared/store";
import { TaskCreate } from "../../../entities/task/types/types";
import { resetForm } from "../../../entities/task/model/slice";

export const handleSubmitS3FileForm = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); // Предотвращаем стандартное поведение сабмита
    const form = event.currentTarget; // Получаем элемент формы

    // Создаем объект FormData из формы
    const formData = new FormData(form);

    try {
        const response = await fetch('https://storage.yandexcloud.net/project-e-bucket', {
            method: 'POST',
            body: formData,
        })
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error('Error during submission:', error);
    }
};



export const useMainTaskFormHandleSubmit = () => {
    const [createTask] = useCreateTaskMutation({
        fixedCacheKey: 'shared-create-task',
      })
    const dispatch = useAppDispatсh()
    const fileNameToPassInGetPresignedUrlForUploadToS3Query = useAppSelector(selectFileNameToGetPresignedUrlFor)
    const handleSubmit = async (formData: TaskCreate) => {
        try {
            const file_extension = fileNameToPassInGetPresignedUrlForUploadToS3Query.split('.').pop()
            const result = await createTask(
                {
                    task_create: formData, 
                    file_extension
                }
            )
            dispatch(resetForm())
        } catch (err) {
            console.log(err)
        }
    }
    return { handleSubmit }
}

