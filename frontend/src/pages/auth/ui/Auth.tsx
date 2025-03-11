import { ChangeEvent, FormEvent, useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useHandleLoginAndRegister } from "../utils/loginAndRegister";
import {
  setAuthError,
  selectAuthError,
  selectCurrentUser,
} from "../../../entities/user/model/user.slice";
import { SuccessAlert } from "../../../shared/ui/Alerts";
import { extendedFormElements } from "../../../shared/types/extendedForm";
import { useAppDispatсh, useAppSelector } from "../../../shared/store";
import { FetchBaseQueryError } from "@reduxjs/toolkit/query";

export const Auth = () => {
  const { authType } = useParams<{ authType: string }>();
  const navigate = useNavigate();
  const [chosenRole, setChosenRole] = useState<string>("teacher");
  const dispatch = useAppDispatсh();
  const authError = useAppSelector(selectAuthError);
  const currentUser = useAppSelector(selectCurrentUser);
  //hook for handling login and register
  const { handleLoginAndRegister, isLoginSuccess, isRegisterSuccess } =
    useHandleLoginAndRegister();
  // clear error on load
  useEffect(() => {
    dispatch(setAuthError(null));
  }, []);
  return (
    <section className="bg-white relative"> {/* Changed the background to white */}
      <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
        {isLoginSuccess && (
          <div className="flex gap-3 flex-col">
            <SuccessAlert mainText={"Вход выполнен"} />
            <div
              className="w-full text-center hover:cursor-pointer"
              onClick={() =>
                navigate(`/${currentUser?.role_type}/variants`, {
                  replace: true,
                })
              }
            >
              Перейти к главной странице
            </div>
          </div>
        )}
        {isRegisterSuccess && (
          <div className="flex flex-col gap-3">
            <SuccessAlert mainText={"Регистрация выполнена"} />
            <div
              className="w-full text-center hover:cursor-pointer"
              onClick={() => {
                navigate("/");
              }}
            >
              Перейти ко входу
            </div>
          </div>
        )}
        {!isLoginSuccess && !isRegisterSuccess && (
          <div className="w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-md xl:p-0 relative"> {/* Removed dark classes*/}
            <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
              <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl"> {/* Removed dark classes*/}
                {authType === "login" ? "Вход в аккаунт" : "Регистрация"}
              </h1>

              <form
                className="space-y-4 md:space-y-6"
                onSubmit={(e: FormEvent<extendedFormElements>) =>
                  handleLoginAndRegister(e, authType)
                }
              >
                <div>
                  <label className="block mb-2 text-sm font-medium text-gray-900"> {/* Removed dark classes*/}
                    Ваш логин
                  </label>
                  <input
                    onFocus={() => dispatch(setAuthError(null))}
                    type="text"
                    name="email"
                    id="email"
                    className="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 "
                    placeholder="user123"
                    required
                  />
                </div>
                <div>
                  <label className="block mb-2 text-sm font-medium text-gray-900"> {/* Removed dark classes*/}
                    Ваш пароль
                  </label>
                  <input
                    onFocus={() => dispatch(setAuthError(null))}
                    type="password"
                    name="password"
                    id="password"
                    placeholder="••••••••"
                    className="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                    required
                  />
                </div>
                {authType === "register" && (
                  <>
                    <div>
                      <label className="block mb-2 text-sm font-medium text-gray-900"> {/* Removed dark classes*/}
                        Ваше имя
                      </label>
                      <input
                        onFocus={() => dispatch(setAuthError(null))}
                        type="text"
                        name="first_name"
                        id="first_name"
                        className="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                        placeholder="Иван"
                        required
                      />
                    </div>
                    <div>
                      <label className="block mb-2 text-sm font-medium text-gray-900"> {/* Removed dark classes*/}
                        Ваша фамилия
                      </label>
                      <input
                        onFocus={() => dispatch(setAuthError(null))}
                        type="text"
                        name="last_name"
                        id="last_name"
                        className="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                        placeholder="Иванов"
                        required
                      />
                    </div>
                    <div>
                      <label className="block mb-2 text-sm font-medium text-gray-900"> {/* Removed dark classes*/}
                        Выберите вашу роль
                      </label>
                      <select
                        onChange={(e: ChangeEvent<HTMLSelectElement>) =>
                          setChosenRole(e.target.value)
                        }
                        value={chosenRole}
                        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                      >
                        <option value="teacher">Учитель</option>
                        <option value="student">Ученик</option>
                      </select>
                    </div>
                    {chosenRole === "teacher" && (
                      <div>
                        <label className="block mb-2 text-sm font-medium text-gray-900"> {/* Removed dark classes*/}
                          Выберите ваш предмет
                        </label>
                        <select className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                          <option value="informatics">Информатика</option>
                          <option value="math">Математика</option>
                          <option value="russian">Русский язык</option>
                          <option value="english">Английский язык</option>
                          <option value="french">Французский язык</option>
                          <option value="spanish">Испанский язык</option>
                          <option value="german">Немецкий язык</option>
                          <option value="history">История</option>
                          <option value="social_studies">Обществознание</option>
                          <option value="geography">География</option>
                          <option value="biology">Биология</option>
                          <option value="chemistry">Химия</option>
                          <option value="physics">Физика</option>
                        </select>
                      </div>
                    )}
                  </>
                )}
                <button
                  type="submit"
                  className="w-full text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
                >
                  {authType === "login" ? "Войти" : "Зарегистрироваться"}
                </button>
                <div className="text-sm font-light text-gray-500 flex flex-row gap-2"> {/* Removed dark classes*/}
                  {authType === "login"
                    ? "Еще нет аккаунта? "
                    : "Уже есть аккаунт? "}
                  <a
                    href="#"
                    className="font-medium text-blue-600 hover:underline"
                    onClick={() =>
                      navigate(
                        `/auth/${
                          authType === "login" ? "register" : "login"
                        }`
                      )
                    }
                  >
                    {authType === "login"
                      ? "Зарегистрироваться"
                      : "Войти"}
                  </a>
                </div>
              </form>
              {authError && (
                <div className="mt-4">
                  <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                    <strong className="font-bold">Ошибка!</strong>
                    {authError.data && typeof authError.data === 'object' && 'message' in authError.data ? (
                      <span className="block sm:inline"> {authError.data.message} </span>
                    ) : (
                      <span className="block sm:inline"> Что-то пошло не так. Пожалуйста, попробуйте еще раз. </span>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </section>
  );
};