import { Link, useNavigate, useSearchParams } from "react-router-dom";
import {
  useAssignVariantToClassroomMutation,
  useAssignVariantToStudentMutation,
  useDeleteVariantMutation,
} from "../api/api";
import { useAppSelector } from "../../../shared/store";
import { selectCurrentUser } from "../../../entities/user/model/user.slice";
import { FaTrash } from "react-icons/fa";

export const Card = ({
  id,
  mainHeader,
  taskAmount,
  subject,
  teacher_name,
}: {
  id: string;
  mainHeader: string;
  taskAmount?: number;
  subject?: string;
  teacher_name?: string;
}) => {
  const [searchParams] = useSearchParams();
  const classroomId = searchParams.get("classroom_id");
  const studentId = searchParams.get("student_id");
  const [assignVariantToClassroom] = useAssignVariantToClassroomMutation();
  const [assignVariantToStudent] = useAssignVariantToStudentMutation();
  const [deleteVariant] = useDeleteVariantMutation();
  const navigate = useNavigate();
  const handleCardClick = async (variant_id: string) => {
    if (!classroomId && !studentId) {
      return;
    }
    if (classroomId) {
      await assignVariantToClassroom({ variant_id, classroom_id: classroomId }).unwrap().then(() => {
        navigate(`../../classes/single/${classroomId}/main-widget`);
      });
      return;
    }
    if (studentId) {
      await assignVariantToStudent({ variant_id, student_id: studentId });
      return;
    }
  };

  const user = useAppSelector(selectCurrentUser);
  return (
    <div
      onClick={() => handleCardClick(id)}
      className="relative w-full sm:max-w-md md:max-w-lg lg:max-w-xl xl:max-w-2xl mx-auto p-6 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
    >
      {/* Иконка удаления */}
      <div
        className="absolute top-2 right-2 p-2 text-gray-500 hover:text-red-500 cursor-pointer transition-colors duration-200"
        onClick={async (e) => {
          e.stopPropagation(); // Останавливаем всплытие события, чтобы не срабатывал handleCardClick
          await deleteVariant({variant_id:id});
        }}
      >
        <FaTrash className="w-5 h-5" />
      </div>

      <a href="#">
        <h5 className="mb-3 text-xl md:text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
          {mainHeader}
        </h5>
      </a>
      <div className="flex flex-col sm:flex-row gap-2 sm:gap-4">
        <p className="font-normal text-gray-700 dark:text-gray-400">
          Кол-во заданий: {taskAmount}
        </p>
        {subject && (
          <p className="font-normal text-gray-700 dark:text-gray-400">
            {subject}
          </p>
        )}
        {teacher_name && (
          <p className="font-normal text-gray-700 dark:text-gray-400">
            {teacher_name}
          </p>
        )}
      </div>
      <Link
        to={`../single/${id}/main-widget`}
        className="mt-4 inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        {user?.role_type == "student" && <p>Перейти к решению</p>}
        {user?.role_type == "teacher" && <p>Перейти к редактированию</p>}
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