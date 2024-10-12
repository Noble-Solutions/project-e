import { ChangeEvent, useEffect, useRef } from "react";
import { useLazyGetPresignedUrlForUploadToS3Query } from "../api/api";
import { useAppDispatсh } from "../../../shared/store";
import { setFileNameToGetPresignedUrlFor } from "../model/slice";
import { handleSubmitS3FileForm, manualFormSubmitTrigger } from "../utils/formHandlers";
export const S3SubmitForm = () => {
    const dispatch = useAppDispatсh()
    const formRef = useRef<HTMLFormElement>(null);
    const[_, result] = useLazyGetPresignedUrlForUploadToS3Query()
    useEffect(() => {
        console.log(result)
    }, [])
    useEffect(() => {
        if (result?.data) {
            console.log(result?.data)
            manualFormSubmitTrigger(formRef)
        }
    }, [result?.data])

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        dispatch(setFileNameToGetPresignedUrlFor(e.target.value))
    }

    return (
        <form 
        ref={formRef}
        onSubmit={handleSubmitS3FileForm}
        action={`https://storage.yandexcloud.net/${result?.data?.bucket_name}`} 
        method="post" 
        encType="multipart/form-data">
            {/* Ключ в хранилище: */}
            <input type="input" name="key" value={result?.data?.key} className="hidden" /><br />
                {/* <!-- Свойства запроса --> */}
            <input type="hidden" name="X-Amz-Credential" value={result?.data?.["X-Amz-Credential"]} />
            <input type="hidden" name="acl" value={result?.data?.acl} />
            <input type="hidden" name="X-Amz-Algorithm" value={result?.data?.["X-Amz-Algorithm"]} />
            <input type="hidden" name="X-Amz-Date" value={result?.data?.["X-Amz-Date"]} />
            <input type="hidden" name="success_action_redirect" value={result?.data?.["success_action_redirect"]} />
            <input type="hidden" name="policy" value={result?.data?.policy} />
            <input type="hidden" name="X-Amz-Signature" value={result?.data?.["X-Amz-Signature"]} />
            {/* <!-- Прочие необходимые поля --> */}
            {/* Файл для загрузки: */}
            <input type="file" name="file" onChange={handleFileChange}/> <br />
            {/* <!-- Поля после “file” игнорируются --> */}
            <input type="submit" name="submit" value="Загрузить" className="hidden"/>
        </form>
    )
}