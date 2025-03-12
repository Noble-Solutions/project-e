import { FormEvent } from "react";
import { useCreateTaskMutation } from "../api/api";
import { selectFileNameToGetPresignedUrlFor, selectAdditionalFilenameToGetPresignedUrlFor } from "../model/slice";
import { useAppDispatсh, useAppSelector } from "../../../shared/store";
import { TaskCreate } from "../../../entities/task/types/types";
import { resetForm } from "../../../entities/task/model/slice";
import { useAddTaskToVariantMutation } from "../../../entities/variant/api/api";
import { useNavigate } from "react-router-dom";
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
        if (response.status !== 204) {
            throw new Error('Failed to upload file');
        }
    } catch (error) {
        console.error('Error during submission:', error);
    }
};



export const useMainTaskFormHandleSubmit = () => {
    const navigate = useNavigate()
    const [createTask] = useCreateTaskMutation({
        fixedCacheKey: 'shared-create-task',
      })
    const [addTaskToVariant] = useAddTaskToVariantMutation()
    const dispatch = useAppDispatсh()

    const fileNameToPassInGetPresignedUrlForUploadToS3Query = useAppSelector(selectFileNameToGetPresignedUrlFor)
    const additionalFileNameToPassInGetPresignedUrlForUploadToS3Query = useAppSelector(selectAdditionalFilenameToGetPresignedUrlFor)
    const handleSubmit = async (formData: TaskCreate, variant_id?: string | null) => {
        try {
            console.log(variant_id)
            const file_extension = fileNameToPassInGetPresignedUrlForUploadToS3Query.split('.').pop()
            const additional_file_extension = additionalFileNameToPassInGetPresignedUrlForUploadToS3Query.split('.').pop()
            await createTask(
                {
                    task_create: formData, 
                    file_extension,
                    additional_file_extension
                }
            ).unwrap().then(async (data) => {
                console.log(data)
                if (variant_id) {
                    await addTaskToVariant({variant_id, task_id: data.task.id})
                    navigate(`../../variants/single/${variant_id}/main-widget`)
                } else {
                    navigate('../../tasks/list')
                }
            })
            dispatch(resetForm())
            
        } catch (err) {
            console.log(err)
        }
    }
    return { handleSubmit }
}

