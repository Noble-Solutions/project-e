import { Card } from "./Card"
import { useGetAllClassroomsOfUserQuery } from "../api/api"
import BackendError from "../../../shared/ui/BackendError"
import { Link } from "react-router-dom"
import { useAppSelector } from "../../../shared/store"
import { selectCurrentUser } from "../../../entities/user/model/user.slice"
export const List = () => {

  const { 
    data: classroomsData, 
    isSuccess: isClassroomsDataSuccess, 
    error: classroomsDataError, 
    isError: isClassroomsDataError 
  } = useGetAllClassroomsOfUserQuery()
  const user = useAppSelector(selectCurrentUser)
  return (
    <div className="flex justify-center w-full lg:w-[84%] lg:mx-auto mt-6 pb-6">
      <div className="flex flex-col gap-4">
        {
        user?.role_type == "teacher" &&
          <Link
          to="../create" 
          relative="path"
          >
              Создать класс
          </Link>
        }
        <div className="grid lg:grid-cols-3 md:grid-cols-2 grid-cols-1 gap-x-10 gap-y-10 ">
            {
            isClassroomsDataSuccess && 
            classroomsData.classrooms.map(
              (classroom) => 
              <Card 
              key={classroom.classroom_data.id}
              id={classroom.classroom_data.id}
              mainHeader={classroom.classroom_data.name} 
              subject={classroom.classroom_data.subject} 
              teacher_first_name={classroom.teacher && classroom.teacher.first_name}
              teacher_last_name={classroom.teacher && classroom.teacher.last_name}
              />
            )
            }
        </div>
      {isClassroomsDataError && <BackendError error={classroomsDataError}/>}
    </div>
  </div>
  )
}

