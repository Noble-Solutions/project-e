import { ChangeEvent, useEffect, useRef } from "react";
import { useCreateTaskMutation } from "../api/api";
import { useAppDispatсh } from "../../../shared/store";
import { setFileNameToGetPresignedUrlFor, setAdditionalFileNameToGetPresignedUrlFor } from "../model/slice";
import { handleSubmitS3FileForm, } from "../utils/formHandlers";
import { manualFormSubmitTrigger } from "../../../shared/utils/utils";

//TODO отрефакторить эту залупу
export const S3SubmitForm = ({number_of_file}: {number_of_file: 1 | 2}) => {
    const dispatch = useAppDispatсh()
    const formRef = useRef<HTMLFormElement>(null);
    const[_, result] = useCreateTaskMutation({
        fixedCacheKey: 'shared-create-task',
      })

    useEffect(() => {
        console.log('triggered')
        if (result?.data) {
            console.log(result?.data)
            if (number_of_file === 1) {
                if ('presigned_url_data_object' in result?.data) {
                    console.log('submitted to s3')
                    console.log(`${result?.data?.presigned_url_data_object?.url}`)
                    manualFormSubmitTrigger(formRef)
                }
            }
            if (number_of_file === 2) {
                if ('additional_presigned_url_data_object' in result?.data) {
                    console.log('submitted to s3')
                    console.log(`${result?.data?.additional_presigned_url_data_object?.url}`)
                    manualFormSubmitTrigger(formRef)
                }
            }
        }
    }, [result?.data])

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        if (number_of_file === 1) {
            dispatch(setFileNameToGetPresignedUrlFor(e.target.value))
        }
        if (number_of_file === 2) {
            dispatch(setAdditionalFileNameToGetPresignedUrlFor(e.target.value))
        }
    }

    return (
        <form 
        ref={formRef}
        onSubmit={handleSubmitS3FileForm}
        >
            {/* Ключ в хранилище: */}
            <input
            type="input" 
            name="key" 
            value={
                number_of_file === 1 ?
                result?.data?.presigned_url_data_object?.fields.key
                : result?.data?.additional_presigned_url_data_object?.fields.key
            } 
            className="hidden" 
            />
            <br />
                {/* <!-- Свойства запроса --> */}
            <input 
            type="hidden" 
            name="X-Amz-Credential" 
            value={
                number_of_file === 1 ? 
                result?.data?.presigned_url_data_object?.fields["x-amz-credential"]
                : result?.data?.additional_presigned_url_data_object?.fields["x-amz-credential"]
            }
            />

            <input 
            type="hidden" 
            name="X-Amz-Algorithm" 
            value={
                number_of_file === 1 ?
                result?.data?.presigned_url_data_object?.fields["x-amz-algorithm"]
                : result?.data?.additional_presigned_url_data_object?.fields["x-amz-algorithm"]
            } 
            />

            <input 
            type="hidden" 
            name="X-Amz-Date" 
            value={
                number_of_file === 1 ?
                result?.data?.presigned_url_data_object?.fields["x-amz-date"]
                : result?.data?.additional_presigned_url_data_object?.fields["x-amz-date"]
            }

            />

            <input 
            type="hidden" 
            name="policy" 
            value={
                number_of_file === 1 ? 
                result?.data?.presigned_url_data_object?.fields.policy
                : result?.data?.additional_presigned_url_data_object?.fields.policy
                
            } 
            />

            <input 
            type="hidden" 
            name="X-Amz-Signature" 
            value={
                number_of_file === 1 ?
                result?.data?.presigned_url_data_object?.fields["x-amz-signature"]
                : result?.data?.additional_presigned_url_data_object?.fields["x-amz-signature"]
            } 
            />
            {/* <!-- Прочие необходимые поля --> */}
            {/* Файл для загрузки: */}
            <input 
            type="file" 
            name="file" 
            onChange={handleFileChange}
            />

            <br />

            {/* <!-- Поля после “file” игнорируются --> */}
            <input 
            type="submit" 
            name="submit" 
            value="Загрузить" 
            className="hidden"
            />
        </form>
    )
}