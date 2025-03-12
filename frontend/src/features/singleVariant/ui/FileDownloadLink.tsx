import { useGetPresignedUrlForGetFromS3Query } from "../../../entities/task/api/api";
import { TaskRead } from "../../../entities/task";
const FileDownloadLink = ({ task }: {task: TaskRead}) => {
  // Используем хук RTK Query для получения presigned URL
  const { data: presignedUrlData, isLoading, isError } = useGetPresignedUrlForGetFromS3Query(
    `${task.additional_file_id}.${task.additional_file_extension}`,
    { skip: !task.additional_file_id } // Пропускаем запрос, если file_id отсутствует
  );

  // Если данные загружаются
  if (isLoading) {
    return <button disabled>Загрузка...</button>;
  }

  // Если произошла ошибка
  if (isError) {
    return <p style={{ color: "red" }}>Ошибка при получении ссылки для скачивания</p>;
  }

  // Если presigned URL получен, отображаем ссылку для скачивания
  return (
    <div>
      {presignedUrlData ? (
        <a href={presignedUrlData} download>
          Скачать файл
        </a>
      ) : (
        <p>Ссылка для скачивания недоступна</p>
      )}
    </div>
  );
};

export default FileDownloadLink;