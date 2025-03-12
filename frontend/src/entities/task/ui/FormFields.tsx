import { selectFormData, setFormData } from "../model/slice";
import { useAppDispatсh, useAppSelector } from "../../../shared/store";
import { ChangeEvent } from "react";

export const FormFields = () => {
  const dispatch = useAppDispatсh();
  const formData = useAppSelector(selectFormData);

  const handleFieldChange = (
    event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = event.target;
    dispatch(setFormData({ [name]: value }));
  };

  return (
    <div className="flex flex-col gap-4">
      {/* gap-4 */}
      <div className="w-full">
        <label
          htmlFor="type"
          className="block mb-2 text-sm font-medium text-gray-700"
        >
          {/* Added label styles */}
          Тип задания
        </label>
        <input
          type="number"
          id="type"
          name="type"
          onChange={handleFieldChange}
          value={formData.type}
          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" // Removed dark classes and changed primary to blue
          placeholder="Type product name"
          required
        />
      </div>
      <div className="w-full">
        <label
          htmlFor="text"
          className="block mb-2 text-sm font-medium text-gray-700"
        >
          {/* Added label styles */}
          Текст задания
        </label>
        <textarea
          id="text"
          onChange={handleFieldChange}
          value={formData.text}
          rows={8}
          name="text"
          className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500" // Removed dark classes and changed primary to blue
          placeholder="Введите описание"
        ></textarea>
      </div>
      <div className="w-full">
        <label
          htmlFor="type_of_answer"
          className="block mb-2 text-sm font-medium text-gray-700"
        >
          {/* Added label styles */}
          Тип ответа
        </label>
        <select
          id="type_of_answer"
          onChange={(e: ChangeEvent<HTMLSelectElement>) =>
            handleFieldChange(e)
          }
          value={formData.type_of_answer}
          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" // Removed dark classes
        >
          <option value="teacher">краткий ответ</option>
          {/* <option value="student">полный ответ</option> */}
        </select>
      </div>
      {formData.type_of_answer === "short_answer" && (
        <div className="w-full">
          <label
            htmlFor="correct_answer"
            className="block mb-2 text-sm font-medium text-gray-700"
          >
            {/* Added label styles */}
            Правильный ответ
          </label>
          <input
            type="text"
            id="correct_answer"
            name="correct_answer"
            required
            onChange={handleFieldChange}
            value={formData.correct_answer}
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" // Removed dark classes and changed primary to blue
            placeholder="Впишите правильный ответ"
          />
        </div>
      )}
    </div>
  );
};

