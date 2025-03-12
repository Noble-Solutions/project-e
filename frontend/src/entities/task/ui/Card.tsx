import { useNavigate, useParams } from "react-router-dom";
import type { TaskRead } from "../../../entities/task";
import { useDeleteTaskMutation, useGetPresignedUrlForGetFromS3Query } from "../api/api";
import { useAddTaskToVariantMutation } from "../../variant/api/api";
import { FaTrash } from "react-icons/fa";

export const Card = (props: TaskRead) => {
    const { variant_id } = useParams();
    const navigate = useNavigate();
    const [addTaskToVariant] = useAddTaskToVariantMutation();

    // Запрос для получения URL картинки
    const { data: presignedUrlData } = useGetPresignedUrlForGetFromS3Query(
        `${props.file_id}.${props.file_extension}`,
        { skip: !props.file_id } // Пропускаем запрос, если file_id отсутствует
    );

    const [deleteTask] = useDeleteTaskMutation();
    // Обработчик клика по карточке
    const handleCardClick = () => {
        if (!variant_id) {
            return;
        }
        addTaskToVariant({ variant_id, task_id: props.id });
        navigate(`../../variants/single/${variant_id}/main-widget`);
    };

    // Заглушка для картинки
    const placeholderImage = "https://dummyimage.com/300x200/cccccc/ffffff&text=No+Image";
    console.log(`presign url data: ${presignedUrlData}`);
    return (
        <div
            onClick={handleCardClick}
            className="max-w-sm rounded-lg overflow-hidden shadow-lg bg-white dark:bg-gray-800 transition-all duration-300 hover:shadow-xl cursor-pointer"
        >
            {/* Image Section */}
            <img
                src={presignedUrlData || placeholderImage} // Используем заглушку, если presignedUrlData отсутствует
                alt="Card Image"
                className="w-full h-48 object-cover"
            />

           

            {/* Content Section */}
            <div className="px-6 py-4 relative">
                 {/* Иконка удаления */}
                 <div
                className="absolute bottom-2 right-2 p-2 text-gray-500 hover:text-red-500 cursor-pointer transition-colors duration-200"
                onClick={async (e) => {
                    e.stopPropagation(); // Останавливаем всплытие события, чтобы не срабатывал handleCardClick
                    await deleteTask({task_id: props.id});
                }}
                >
                    <FaTrash className="w-5 h-5" />
                </div>
                {/* Type */}
                <p className="text-gray-700 dark:text-gray-300 text-sm font-semibold mb-2">
                    {props.type}
                </p>

                {/* Text */}
                <p className="text-gray-900 dark:text-white text-lg font-bold mb-2">
                    {props.text}
                </p>

                {/* Correct Answer (Conditional) */}
                {props.correct_answer && (
                    <p className="text-green-600 dark:text-green-400 text-sm">
                        Правильный ответ: {props.correct_answer}
                    </p>
                )}
            </div>
        </div>
    );
};