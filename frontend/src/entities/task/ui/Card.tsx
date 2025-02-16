import { useNavigate, useParams } from "react-router-dom";
import type { TaskRead } from "../../../entities/task";
import { useGetPresignedUrlForGetFromS3Query } from "../api/api";
import { useAddTaskToVariantMutation } from "../../variant/api/api";
export const Card = (props: TaskRead) => {
    const { variant_id } = useParams()
    const navigate = useNavigate()
    const [addTaskToVariant] = useAddTaskToVariantMutation()
    const { 
        data: presignedUrlData
    } = useGetPresignedUrlForGetFromS3Query(
        `${props.file_id}.${props.file_extension}`, 
        {skip: !props.file_id})
    
    const handleCardClick = () => {
        if (!variant_id) {
            return
        }
        addTaskToVariant({variant_id, task_id: props.id})
        navigate(`../../variants/single/${variant_id}/main-widget`)
    }

    return (
        <div 
        onClick={handleCardClick}
        className="max-w-sm rounded-lg overflow-hidden shadow-lg bg-white dark:bg-gray-800 transition-all duration-300 hover:shadow-xl">
            {/* Image Section */}
            <img
                src={presignedUrlData}
                alt="Card Image"
                className="w-full h-48 object-cover"
            />

            {/* Content Section */}
            <div className="px-6 py-4">
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
}