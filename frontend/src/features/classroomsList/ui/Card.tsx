import { useEffect, useState } from "react";
import { formatName } from "../utils/utils";
import { Link } from "react-router-dom";
import { FaTrash } from "react-icons/fa";
import { useDeleteClassroomMutation } from "../api/api";

export const Card = ({
  mainHeader,
  subject,
  id,
  teacher_first_name,
  teacher_last_name,
}: {
  mainHeader: string;
  id: string;
  subject?: string;
  teacher_first_name?: string;
  teacher_last_name?: string;
}) => {
  const [teacherName, setTeacherName] = useState<string | null>(null);
  const [deleteClassroom] = useDeleteClassroomMutation();
  useEffect(() => {
    if (teacher_first_name && teacher_last_name) {
      setTeacherName(formatName(`${teacher_first_name} ${teacher_last_name}`));
    }
  }, [teacher_first_name, teacher_last_name]); // Add dependencies for useEffect

  return (
    <div className="relative w-full sm:max-w-md md:max-w-lg lg:max-w-xl mx-auto p-6 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
        {/* Added max-width to div */}
      
      {/* Иконка удаления */}
            <div
              className="absolute top-2 right-2 p-2 text-gray-500 hover:text-red-500 cursor-pointer transition-colors duration-200"
              onClick={async (e) => {
                e.stopPropagation(); // Останавливаем всплытие события, чтобы не срабатывал handleCardClick
                await deleteClassroom({classroom_id:id});
              }}
            >
              <FaTrash className="w-5 h-5" />
            </div>

      <a href="#">
        <h5 className="mb-3 text-xl md:text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
          {mainHeader}
        </h5>
          {/* Changed to text-xl, added md:text-2xl, changed mb-2 to mb-3 */}
      </a>
      <div className="flex flex-col gap-2">
        {/* Added gap-2 for spacing */}
        {subject && (
          <p className="font-normal text-gray-700 dark:text-gray-400">
            {subject}
          </p>
        )}
        {teacherName && (
          <p className="font-normal text-gray-700 dark:text-gray-400">
            {teacherName}
          </p>
        )}
      </div>
      <Link
        to={`../single/${id}/main-widget`}
        className="mt-4 inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" // Added mt-4
      >
        Перейти в класс
        <svg
          className="rtl:rotate-180 w-3.5 h-3.5 ms-2"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 14 10"
        >
          <path
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M1 5h12m0 0L9 1m4 4L9 9"
          />
        </svg>
      </Link>
    </div>
  );
};