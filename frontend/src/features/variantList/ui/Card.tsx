import { Link, useSearchParams } from "react-router-dom";
import {
  useAssignVariantToClassroomMutation,
  useAssignVariantToStudentMutation,
} from "../api/api";
import { useAppSelector } from "../../../shared/store";
import { selectCurrentUser } from "../../../entities/user/model/user.slice";

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

  const handleCardClick = async (variant_id: string) => {
    if (!classroomId && !studentId) {
      return;
    }
    if (classroomId) {
      await assignVariantToClassroom({ variant_id, classroom_id: classroomId });
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
      className="w-full sm:max-w-md md:max-w-lg lg:max-w-xl xl:max-w-2xl mx-auto p-6 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700" // Added responsive width, max-width, and margin
    >
      <a href="#">
        <h5 className="mb-3 text-xl md:text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
          {mainHeader}
        </h5> {/* Reduced mb, added md:text-2xl for larger screens */}
      </a>
      <div className="flex flex-col sm:flex-row gap-2 sm:gap-4"> {/* Made the info flex on larger screens, added gap */}
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
        className="mt-4 inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" // Added mt-4
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