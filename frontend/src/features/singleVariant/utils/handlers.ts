import { useRemoveTaskFromVariantMutation } from "../../../entities/variant/api/api"
import { useCheckVariantMutation } from "../api/api"

export const useHandleSingleVariantMutations = () => {
        const [ removeTaskFromVariant ] = useRemoveTaskFromVariantMutation()
        const [checkVariant] = useCheckVariantMutation({fixedCacheKey: 'shared-check-variant'})
        const handleRemoveTaskFromVariant = async (variant_id: string | undefined, task_id: string | undefined) => {
            try {
                if (!variant_id) {
                    throw new Error('variant_id is undefined')
                }
                if (!task_id) {
                    throw new Error('task_id is undefined')
                }
                await removeTaskFromVariant({variant_id, task_id})
            } catch (err) {
                console.log(err)
            }
        }

        const handleCheckVariant = async (variant_id: string | undefined, answers: {[key: string]: string}) => {
            try {
                if (!variant_id) {
                    throw new Error('variant_id is undefined')
                }
                await checkVariant({variant_id, answers})
            } catch (err) {
                console.log(err)
            }
        }
        return { handleRemoveTaskFromVariant, handleCheckVariant }
}