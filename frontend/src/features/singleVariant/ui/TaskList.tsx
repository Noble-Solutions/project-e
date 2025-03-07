import { skipToken } from "@reduxjs/toolkit/query"
import { useGetVariantByIdWithTasksQuery } from "../api/api"
import { useLocation, useNavigate, useParams } from "react-router-dom"
import { AddTaskDropdown } from "./AddTaskDropdown"
import BackendError from "../../../shared/ui/BackendError"
import { useEffect } from "react"
import { useHandleSingleVariantMutations } from "../utils/handlers"
import { useAppSelector } from "../../../shared/store"
import { selectCurrentUser } from "../../../entities/user/model/user.slice"
import { useAppDispatсh } from "../../../shared/store"
import { selectVariantAnswers, selectAnswerToTask, addAnswerToTask } from "../model/slice"
import { useGetPresignedUrlForGetFromS3Query } from "../../../entities/task/api/api"
import { SingleTask } from "./SingleTask"
export const TaskList = () => {
    const { id } = useParams<{id: string}>()
    const { data: variant, isSuccess: isGetVariantSuccess, error: getVariantError, isError: isGetVariantError } = useGetVariantByIdWithTasksQuery(id || skipToken)
    const navigate = useNavigate()
    const location = useLocation()
    const { task_id } = useParams()
    const { handleRemoveTaskFromVariant, handleCheckVariant } = useHandleSingleVariantMutations()
    const user = useAppSelector(selectCurrentUser)
    const dispatch = useAppDispatсh()
    
    const answerToCurrentTask = useAppSelector((state) =>selectAnswerToTask(state,task_id))
    const answersToVariant = useAppSelector(selectVariantAnswers)
    console.log(answerToCurrentTask)
    useEffect(() => {
        if (variant && variant.tasks.length > 0) {
            const currentPath = location.pathname;
            if (currentPath.endsWith('/main-widget')) {
                const newPath = `${currentPath}/${variant.tasks[0].id}`;
                navigate(newPath);
            }
            
            
        }
    }, [variant])

    return (
        <div className=" h-full">
            {isGetVariantSuccess && 
            <div className="mb-4 flex flex-col gap-2">
                <p className="text-2xl text-center">{variant.variant_data.name}</p>
                
                <div className="flex flex-row justify-center items-center gap-[20rem]">
                {user?.role_type == "teacher" &&
                    <>
                        <button 
                        onClick={() => handleRemoveTaskFromVariant(id, task_id)}
                        className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
                            Удалить задание
                        </button>
                        <AddTaskDropdown id={id} />
                    </>
                }
                {
                    user?.role_type == "student" &&
                    <button 
                    onClick={() => {
                        handleCheckVariant(id, answersToVariant, variant.variant_data?.classroom_id)
                        navigate('../variant-results')
                    }}
                    className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
                        Завершить выполнение
                    </button>
                }
                </div>
            </div>
            }
            
            {isGetVariantError && <BackendError error={getVariantError}/>}
            {isGetVariantSuccess &&
                <div className="flex flex-col md:flex-row gap-4 py-4 h-[70%]">
                {/* Left Section */}
                <div className="flex flex-col text-2xl justify-start items-center md:w-1/10">
                    {variant.tasks.map((task) => (
                        <div 
                        key={task.id} 
                        onClick={() => navigate(`../main-widget/${task.id}`)}
                        className=" pt-2 border-b-2 solid border-black w-full hover:bg-gray-200 hover:cursor-pointer px-4">
                            <p className="text-center">{task.type}</p>
                        </div>
                    ))}
                </div>
            
                {/* Right Section */}
                <div className="flex-row justify-stretch h-full w-full items-center">
                    <div className="flex flex-col gap-4 w-full h-4/5 justify-start items-center">
                        {variant.tasks
                            .filter((task) => task.id == task_id)
                            .map((task) => (
                                <SingleTask {...task} />
                            ))}
                    </div>
                    {user?.role_type == "student" &&
                        <div className="flex flex-row gap-3 h-1/5 justify-end items-end pr-5">
                            <div>
                                <input
                                value={answerToCurrentTask}
                                onChange={(e) => dispatch(addAnswerToTask({task_id: task_id, answer: e.target.value}))}
                                placeholder="Ваш ответ"
                                type="text"  
                                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"/>
                            </div>
                        </div>
                    }
                </div>
            </div>
            }
            
        </div>
        
    )
}