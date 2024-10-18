import { selectFormData, setFormData } from "../model/slice"
import { useAppDispatсh, useAppSelector } from "../../../shared/store"
import { ChangeEvent } from "react"
export const FormFields = () => {
    const dispatch = useAppDispatсh()
    const formData = useAppSelector(selectFormData)

    const handleFieldChange = (event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = event.target
        dispatch(setFormData({[name]: value }))
    }

    return (
        <>
            <div className="flex flex-col">
                <div className="w-full">
                    <label>
                        Тип задания
                        <input 
                        type="number" 
                        name="type"
                        onChange={handleFieldChange}
                        value={formData.type}
                        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" 
                        placeholder="Type product name" 
                        required={true} />
                    </label>
                </div>
                <div className="w-full">
                    <label>
                        Текст задания
                        <textarea
                        onChange={handleFieldChange}
                        value={formData.text}
                        rows={8} 
                        name="text"
                        className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" 
                        placeholder="Your description here">
                        </textarea>
                    </label>
                </div>
                <div className="w-full">
                    <label>
                        Тип ответа
                        <input 
                        type="text" 
                        name="type_of_answer" 
                        required={true}
                        onChange={handleFieldChange}
                        value={formData.type_of_answer}
                        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" 
                        placeholder="$2999"
                        />
                    </label>
                </div>
                {formData.type_of_answer === 'short_answer' &&
                    <div className="w-full">
                        <label>
                            Правильный ответ
                            <input 
                            type="text" 
                            name="correct_answer" 
                            required={true}
                            onChange={handleFieldChange}
                            value={formData.correct_answer}
                            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" 
                            placeholder="Впишите правильный ответ"
                            />
                        </label>
                    </div>
                }
            </div>
        </>
    )
}

