import { TaskRead } from "../../../entities/task"
import { useGetPresignedUrlForGetFromS3Query } from "../../../entities/task/api/api";

export const SingleTask = (task: TaskRead) => {
    const placeholderImage = "https://dummyimage.com/300x200/cccccc/ffffff&text=No+Image";
    const { data: presignedUrlData } = useGetPresignedUrlForGetFromS3Query(
            `${task.file_id}.${task.file_extension}`,
            { skip: !task.file_id, } // Пропускаем запрос, если file_id отсутствует
        );
    console.log(presignedUrlData)
    return (
        <>
            <div className="flex justify-center items-center w-full h-96"> {/* Контейнер для центрирования */}
                <img
                    key={task.file_id ? `${task.file_id}.${task.file_extension}` : "placeholder"}
                    src={!task.file_id ? placeholderImage : presignedUrlData}
                    alt="Card Image"
                    className="max-w-full max-h-full object-contain" // Ограничение по ширине и высоте
                />
            </div>
            <div key={task.id} className="text-center">
                <p>Текст задания: {task.text}</p>
                <p>Тип задания: {task.type}</p>
            </div>
        </>
    )
    }

