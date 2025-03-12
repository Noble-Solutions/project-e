import { Link } from "react-router-dom";
import { useGetAllTasksOfTeacherQuery } from "../api/api";
import { TaskCard } from "../../../entities/task";

export const List = () => {
  const {
    data: tasksListData,
    isSuccess: isTasksListDataSuccess,
    isError: isTasksListDataError,
  } = useGetAllTasksOfTeacherQuery();

  return (
    <div className="container mx-auto px-4 py-8"> {/* Container for responsiveness */}
      <div className="flex flex-col gap-6"> {/* Increased gap */}
        <div className="w-full flex justify-center"> {/* Center the button */}
          <Link
            to="../create"
            relative="path"
            className="inline-flex items-center px-5 py-2.5 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
          >
            Создать задание
          </Link>
        </div>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {/* Responsive grid */}
          {isTasksListDataError &&  
            <div className="flex justify-center items-center p-6">
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
                        <strong className="font-bold">Ошибка!</strong>
                        <span className="block sm:inline">
                            {' '}
                            Что-то пошло не так. Пожалуйста, попробуйте еще раз.
                        </span>
                    </div>
            </div>
            }
          {isTasksListDataSuccess &&
            tasksListData.map((task) => (
              <TaskCard key={task.id} {...task} />
            ))}
        </div>
      </div>
    </div>
  );
};