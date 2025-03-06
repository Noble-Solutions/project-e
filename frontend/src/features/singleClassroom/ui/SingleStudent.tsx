import { useParams } from "react-router-dom"
import { useGetClassroomByIdWithStudentsAndTeacherQuery, useGetStudentPerformanceQuery } from "../api/api"
import { skipToken } from "@reduxjs/toolkit/query"

export const SingleStudent = () => {
    const { student_id } = useParams()

    // classroom_id
    const { id } = useParams()

    const { data: studentPerformance, isSuccess, isError } = useGetStudentPerformanceQuery({classroom_id: id, student_id})
    const { data: classroomData} = useGetClassroomByIdWithStudentsAndTeacherQuery(id || skipToken)
    
    // Функция для вычисления процента верно решенных заданий
        // Функция для вычисления процента верно решенных заданий
        // Функция для вычисления процента верно решенных заданий
    const calculatePercentage = (correct: number, total: number): number => {
        if (total === 0) return 0;
        return (correct / total) * 100;
    };

    // Вычисляем tasksWithPercentage только если данные успешно загружены
    const tasksWithPercentage = isSuccess
        ? studentPerformance.map((task) => ({
              ...task,
              percentage: calculatePercentage(
                  task.task_stat.correct_solved,
                  task.task_stat.total_solved
              ),
          }))
        : [];

    // Фильтруем задания для лучшего и худшего (только те, где total_solved > 10)
    const filteredTasks = tasksWithPercentage.filter(
        (task) => task.task_stat.total_solved > 10
    );

    // Лучшее и худшее задание (если есть минимум два задания с total_solved > 10)
    let bestTasks: number[] = [];
    let worstTasks: number[] = [];
    let bestPercentage = 0;
    let worstPercentage = 0;

    if (filteredTasks.length >= 2) {
        // Находим лучшее задание (максимальный процент)
        bestPercentage = Math.max(...filteredTasks.map((task) => task.percentage));
        bestTasks = filteredTasks
            .filter((task) => task.percentage === bestPercentage)
            .map((task) => task.task_stat.task_type);

        // Находим худшее задание (минимальный процент)
        worstPercentage = Math.min(...filteredTasks.map((task) => task.percentage));
        worstTasks = filteredTasks
            .filter((task) => task.percentage === worstPercentage)
            .map((task) => task.task_stat.task_type);
    }

    return (
        <div className="p-4">
            {isSuccess && (
                <div className="flex flex-col gap-5">
                        <p className="text-2xl w-full text-center">
                        {
                            classroomData?.students.find((student) => student.id === student_id)?.first_name + ' ' + classroomData?.students.find((student) => student.id === student_id)?.last_name
                        }
                        </p>
                    
                    {/* Таблица */}
                    <div className="overflow-x-auto mb-8">
                        <table className="min-w-full bg-white border border-gray-200">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Тип задания
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Всего решено
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Решено верно
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        % верно решенных
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-200">
                                {tasksWithPercentage.map((task) => (
                                    <tr key={task.task_stat.id}>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                            {task.task_stat.task_type}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                            {task.task_stat.total_solved}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                            {task.task_stat.correct_solved}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                            {task.percentage.toFixed(2)}%
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    {/* Лучшее и худшее задание (если есть минимум два задания с total_solved > 10) */}
                    {filteredTasks.length >= 2 ? (
                        <div className="space-y-4">
                            <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
                                <strong>Лучшее задание:</strong>{' '}
                                {bestTasks.join(', ')} (Процент решения: {bestPercentage.toFixed(2)}%)
                            </div>
                            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                                <strong>Худшее задание:</strong>{' '}
                                {worstTasks.join(', ')} (Процент решения: {worstPercentage.toFixed(2)}%)
                            </div>
                        </div>
                    ) : (
                        <div className="text-center text-gray-600">
                            Чтобы увидеть статистику по лучшему и худшему заданию, у ученика должно быть решено 2 типа заданий больше 10 раз.
                        </div>
                    )}
                </div>
            )}
            {isError && (
                <div className="flex justify-center items-center p-6">
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
                        <strong className="font-bold">Ошибка!</strong>
                        <span className="block sm:inline">
                            {' '}
                            Что-то пошло не так. Пожалуйста, попробуйте еще раз.
                        </span>
                    </div>
                </div>
            )}
        </div>
    );
};