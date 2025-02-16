import { useEffect, useState } from "react"
import { useGetStudentByUsernameMutation, useAddStudentToClassroomMutation } from "../api/api"
import { IoIosAddCircleOutline } from "react-icons/io";
import { useNavigate, useParams } from "react-router-dom";
export const AddStudent = () => {
    const id = useParams<string>()
    const navigate = useNavigate()
    const [getStudentByUsername, result] = useGetStudentByUsernameMutation()
    const [addStudentToClassroom, resultOfAddStudentToClassroom] = useAddStudentToClassroomMutation()
    const [searchFieldValue, setSearchFieldValue] = useState<string>('')
    const handleSearchButtonClick = async () => {
        try {
            await getStudentByUsername(searchFieldValue).unwrap()
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

    useEffect(() => {
        if (resultOfAddStudentToClassroom.isSuccess) {
            navigate(`../main-widget`)
        }
    }, [resultOfAddStudentToClassroom.isSuccess])

    const handleAddStudentButtonClick = async () => {
        try {
            if (!result.data) {
                return
            }
            if (!id.id) {
                return
            }
            console.log({student_id: result.data.id, classroom_id: id.id})
            await addStudentToClassroom({student_id: result.data.id, classroom_id: id.id}).unwrap()
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

    


    return (
        <div className="w-full flex flex-col gap-4">
            <div className="w-[50%] mx-auto">   
                <label className="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
                <div className="relative">
                    <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                        <svg className="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
                        </svg>
                    </div>
                    <input 
                    value={searchFieldValue}
                    onChange={(e) => setSearchFieldValue(e.target.value)}
                    className="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" 
                    placeholder="Введите имя пользователя ученика" 
                    required 
                    />
                    <button 
                    onClick={handleSearchButtonClick}
                    className="text-white absolute end-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Search</button>
                </div>
            </div>
            {result.isSuccess &&
            <div className="flex flex-row justify-between items-center p-2 border-black border-opacity-20 border-2 rounded-lg shadow-xl mx-12">
                        <p className="">
                            {result.data.first_name} {result.data.last_name}
                        </p>
                        <IoIosAddCircleOutline onClick={handleAddStudentButtonClick}/>
            </div>
            }
        </div> 
    )
}


