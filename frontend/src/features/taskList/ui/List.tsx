import { Link } from "react-router-dom";
import { useGetAllTasksOfTeacherQuery } from "../api/api";
import { TaskCard } from "../../../entities/task";
import BackendError from "../../../shared/ui/BackendError";

export const List = () => {
  const {
    data: tasksListData,
    isSuccess: isTasksListDataSuccess,
    error: tasksListDataError,
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
          {isTasksListDataError && <BackendError error={tasksListDataError} />}
          {isTasksListDataSuccess &&
            tasksListData.map((task) => (
              <TaskCard key={task.id} {...task} />
            ))}
        </div>
      </div>
    </div>
  );
};