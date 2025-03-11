import { TaskFormFields } from "../../../entities/task";
import { S3SubmitForm } from "./s3SubmitForm";
import { useMainTaskFormHandleSubmit } from "../utils/formHandlers";
import { useEffect, useRef } from "react";
import { selectFormData } from "../../../entities/task";
import { useAppSelector } from "../../../shared/store";
import { manualFormSubmitTrigger } from "../../../shared/utils/utils";
import { useParams } from "react-router-dom";

export const MainTaskForm = () => {
  const formRef = useRef<HTMLFormElement>(null);
  const { handleSubmit } = useMainTaskFormHandleSubmit();
  const formData = useAppSelector(selectFormData);

  const { variant_id } = useParams();
  useEffect(() => {
    console.log(variant_id);
  }, [variant_id]); // Added variant_id to dependencies

  return (
    <div className="flex flex-col gap-6 w-full">
      {/* flex container for responsiveness */}
      <form
        ref={formRef}
        onSubmit={() => handleSubmit(formData, variant_id || null)}
        className="w-full"
      >
        {/*Added w-full */}
        <TaskFormFields />
      </form>
      <div className="w-full">
        <S3SubmitForm />
      </div>
      <div className="w-full flex justify-center">
        <button
          onClick={() => manualFormSubmitTrigger(formRef)}
          type="button"
          className="w-full sm:w-auto text-white bg-blue-600 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
        >
          Создать задание
        </button>
      </div>
    </div>
  );
};