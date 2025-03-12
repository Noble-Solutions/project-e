import { useGetPresignedUrlForGetFromS3Query } from "../../../entities/task/api/api";
import { TaskRead } from "../../../entities/task";
import { FaFileDownload } from "react-icons/fa"; // Импортируем иконку файла

const FileDownloadLink = ({ task }: { task: TaskRead }) => {
  // Используем хук RTK Query для получения presigned URL
  const { data: presignedUrlData, isLoading, isError } = useGetPresignedUrlForGetFromS3Query(
    `${task.additional_file_id}.${task.additional_file_extension}`,
    { skip: !task.additional_file_id } // Пропускаем запрос, если file_id отсутствует
  );

  // Если данные загружаются
  if (isLoading) {
    return (
      <button
        className="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500 cursor-not-allowed"
        disabled
      >
        <FaFileDownload className="text-lg" />
        Загрузка...
      </button>
    );
  }

  // Если произошла ошибка
  if (isError) {
    return <p className="text-red-500 font-medium">Ошибка при получении ссылки для скачивания</p>;
  }

  // Если presigned URL получен, отображаем ссылку для скачивания
  return (
    <div className="flex items-center gap-2">
      {presignedUrlData ? (
        <a
          href={presignedUrlData}
          download={`${task.type}.${task.additional_file_extension}`}
          className="flex items-center gap-2 px-3 py-2 text-blue-700 font-medium border border-blue-700 rounded-md transition-colors hover:bg-blue-700 hover:text-white"
        >
          <FaFileDownload className="text-lg" />
          Скачать {task.type}.{task.additional_file_extension}
        </a>
      ) : (
        <p className="text-gray-500 font-medium">Ссылка для скачивания недоступна</p>
      )}
    </div>
  );
};

export default FileDownloadLink;