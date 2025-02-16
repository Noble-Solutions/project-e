import { skipToken } from "@reduxjs/toolkit/query"
import { useGetClassroomByIdWithStudentsAndTeacherQuery } from "../api/api"
import { Link, useParams } from "react-router-dom"
import { StudentCard } from "./StudentCard"

export const MainList = () => {
    const { id } = useParams<{id: string}>()
    const { data: classroom, isSuccess: isGetClassroomSuccess } = useGetClassroomByIdWithStudentsAndTeacherQuery(id || skipToken)
    
    return (
        <div>
            {isGetClassroomSuccess && 
            <div className="mb-4 flex flex-col gap-2">
            <p className="text-2xl text-center">{classroom.classroom_data.name}</p>
            <div className="flex flex-row justify-center items-center gap-[20rem]">
            <Link to={`../../../variants/list?classroom_id=${id}`} className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
                Назначить вариант
            </Link>
            <Link to="../add-student" className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
                Добавить ученика
            </Link>
            </div>
            </div>
            }
            <ul className=" mx-12 flex flex-col gap-2">
                {isGetClassroomSuccess && 
                classroom.students.map((student) => <StudentCard student={student} key={student.id}/>)
                }
            </ul>
        </div>
        
    )
}