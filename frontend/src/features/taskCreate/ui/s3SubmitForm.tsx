import { ChangeEvent, useEffect, useRef } from "react";
import { useCreateTaskMutation } from "../api/api";
import { useAppDispatсh } from "../../../shared/store";
import { setFileNameToGetPresignedUrlFor } from "../model/slice";
import { handleSubmitS3FileForm, } from "../utils/formHandlers";
import { manualFormSubmitTrigger } from "../../../shared/utils/utils";

//TODO отрефакторить эту залупу
export const S3SubmitForm = () => {
    const dispatch = useAppDispatсh()
    const formRef = useRef<HTMLFormElement>(null);
    const[_, result] = useCreateTaskMutation({
        fixedCacheKey: 'shared-create-task',
      })

    useEffect(() => {
        console.log('triggered')
        if (result?.data) {
            console.log(result?.data)
            if ('presigned_url_data_object' in result?.data) {
                console.log('submitted to s3')
                console.log(`${result?.data?.presigned_url_data_object?.url}`)
                manualFormSubmitTrigger(formRef)
            }
        }
    }, [result?.data])

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        dispatch(setFileNameToGetPresignedUrlFor(e.target.value))
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
            value={result?.data?.presigned_url_data_object?.fields.key} 
            className="hidden" 
            />
            <br />
                {/* <!-- Свойства запроса --> */}
            <input 
            type="hidden" 
            name="X-Amz-Credential" 
            value='gbcz' 
            />

            <input 
            type="hidden" 
            name="X-Amz-Algorithm" 
            value={result?.data?.presigned_url_data_object?.fields["x-amz-algorithm"]} 
            />

            <input 
            type="hidden" 
            name="X-Amz-Date" 
            value={result?.data?.presigned_url_data_object?.fields["x-amz-date"]} 
            />

            <input 
            type="hidden" 
            name="policy" 
            value={result?.data?.presigned_url_data_object?.fields.policy} 
            />

            <input 
            type="hidden" 
            name="X-Amz-Signature" 
            value={result?.data?.presigned_url_data_object?.fields["x-amz-signature"]} 
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