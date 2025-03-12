import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { SuccessAlert } from '../../../shared/ui/Alerts';
import { useHandleCreateVariant } from '../utils/formHandler';
import { FormEvent } from 'react';
import { extendedFormElements } from '../../../shared/types/extendedForm';

export const CRUDForm = () => {
  const navigate = useNavigate();
  const { handleCreateVariant, isCreateVariantSuccess, isLoadingVariant } = useHandleCreateVariant(); // Assuming isLoading is available

  const [formData, setFormData] = useState({
    name: '', // Initialize with empty values
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

    const handleSubmit = (e: FormEvent<extendedFormElements>) => {
        e.preventDefault();
        handleCreateVariant(e)
    }

  return (
    <section className="bg-white py-12"> {/* Changed to white background */}
      <div className="container mx-auto px-4">
        <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg overflow-hidden"> {/* Removed dark mode classes */}
          {isCreateVariantSuccess ? (
            <div className="p-8 flex flex-col gap-4 items-center justify-center">
              <SuccessAlert mainText={'Вариант успешно создан'} />
              <button
                onClick={() => navigate(`/teacher/variants/list`, { replace: true })}
                className="w-full sm:w-auto px-5 py-2.5 text-center text-white bg-blue-600 hover:bg-blue-700 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Перейти к странице вариантов
              </button>
            </div>
          ) : (
            <div className="p-8">
              <h2 className="text-3xl font-bold text-gray-800 mb-6"> {/* Removed dark mode classes */}
                Создать новый вариант
              </h2>
              <form className="space-y-6" onSubmit={handleSubmit}>
                {/* Variant Name */}
                <div>
                  <label htmlFor="name" className="block mb-2 text-sm font-medium text-gray-700"> {/* Removed dark mode classes */}

                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" // Removed dark mode classes
                    placeholder="Название варианта"
                    required
                  />
                </div>
                <button
                  type="submit"
                  disabled={isLoadingVariant}
                  className="w-full text-white bg-blue-600 hover:bg-blue-700 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 px-5 py-2.5 text-center disabled:bg-blue-400"
                >
                  {isLoadingVariant ? 'Создание...' : 'Создать вариант'}
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};