import { Card } from "./Card";
import { useGetAllClassroomsOfUserQuery } from "../api/api";
import BackendError from "../../../shared/ui/BackendError";
import { Link } from "react-router-dom";
import { useAppSelector } from "../../../shared/store";
import { selectCurrentUser } from "../../../entities/user/model/user.slice";

export const List = () => {
  const {
    data: classroomsData,
    isSuccess: isClassroomsDataSuccess,
    error: classroomsDataError,
    isError: isClassroomsDataError,
  } = useGetAllClassroomsOfUserQuery();
  const user = useAppSelector(selectCurrentUser);

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Container for responsiveness */}
      <div className="flex flex-col gap-6">
        {/* Increased gap */}
        {user?.role_type === "teacher" && (
          <div className="w-full flex justify-center">
          {/* Center the button */}
            <Link
              to="../create"
              relative="path"
              className="inline-flex items-center px-5 py-2.5 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              Создать класс
            </Link>
          </div>
        )}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {/* Responsive grid */}
          {isClassroomsDataSuccess &&
            classroomsData.classrooms.map((classroom) => (
              <Card
                key={classroom.classroom_data.id}
                id={classroom.classroom_data.id}
                mainHeader={classroom.classroom_data.name}
                subject={classroom.classroom_data.subject}
                teacher_first_name={
                  classroom.teacher && classroom.teacher.first_name
                }
                teacher_last_name={
                  classroom.teacher && classroom.teacher.last_name
                }
              />
            ))}
          {isClassroomsDataError && (
            <BackendError error={classroomsDataError} />
          )}
        </div>
      </div>
    </div>
  );
};

