import { FormEvent } from "react"
import { useCreateVariantMutation } from "../api/api"
import { extendedFormElements } from "../../../shared/types/extendedForm"


export const useHandleCreateVariant = () => {
    const [createVariant, { isSuccess: isCreateVariantSuccess, isLoading: isLoadingVariant }] = useCreateVariantMutation()
    const handleCreateVariant = async (e: FormEvent<extendedFormElements>): Promise<void> => {
        e.preventDefault()
        const { elements } = e.currentTarget
        const name = elements[0].value
        const VariantCreateData: {name: string} = {
            name
        }
        try {
            console.log(VariantCreateData)
            await createVariant(VariantCreateData).unwrap()
            .then((data) => {
                console.log(data)
                
            })
        }  catch (err: any) {
                if ('data' in err && 'status' in err) {
                    console.log(err.data)
                } else {
                    console.log(err)
                }
            }
        }
        return { handleCreateVariant, isCreateVariantSuccess, isLoadingVariant }
    }