import { useNavigate } from "react-router-dom"
import { SuccessAlert } from "../../../shared/ui/Alerts"
import { useHandleCreateClassroom } from "../utils/formHandler"
import { FormEvent } from "react"
import { extendedFormElements } from "../../../shared/types/extendedForm"
export const CRUDForm = () => {
    const navigate = useNavigate()
    const { handleCreateClassroom, isCreateCLassroomSuccess } = useHandleCreateClassroom()
    return (
        <section className="bg-gray-50 dark:bg-gray-900 relative">
            <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
                    {
                    isCreateCLassroomSuccess &&
                    <div className="flex gap-3 flex-col">
                        <SuccessAlert mainText={'Класс успешно создан'}/>
                        <div 
                        className="w-full text-center hover:cursor-pointer"
                        onClick={() => navigate(`/teacher/classes/list`, {replace: true})}>
                            Перейти к странице классов
                        </div>
                    </div>
                    }
                    { !isCreateCLassroomSuccess &&
                        <div className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
                            <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
                                <form className="space-y-4 md:space-y-6" onSubmit={(e: FormEvent<extendedFormElements>) => handleCreateClassroom(e)}>
                                    <div>
                                        <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Название класса</label>
                                        <input 
                                        type="text" 
                                        name="email"
                                        className="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" 
                                        placeholder="Информатика 11Е" 
                                        required={true}/>
                                    </div>
                                    <button type="submit" className="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">
                                        Создать класс
                                    </button>
                                </form>
                            </div>
                        </div>
                    }
            </div>
        </section>
    )
}