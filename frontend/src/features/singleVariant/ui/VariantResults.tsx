import { useCheckVariantMutation } from "../api/api"

export const VariantResults = () => {
    const [_, result] = useCheckVariantMutation({fixedCacheKey: 'shared-check-variant'})
  return (
    <>
        {
            result.isSuccess && 
            <div>
                <p>Ваш вариант проверен</p>
                <p>Баллов набрано {result?.data?.points_earned_by_student} из {result?.data?.maximum_points}</p>
            </div>
        }
    </>
  )
}


