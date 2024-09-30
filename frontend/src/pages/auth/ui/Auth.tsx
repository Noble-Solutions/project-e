import { FormEvent} from "react"
import { useParams, useNavigate } from "react-router-dom"


import { useHandleLoginAndRegister } from "../utils/loginAndRegister"

import { setAuthError, selectAuthError, selectCurrentUser } from "../../../entities/user/model/user.slice";

import BackendError from "../../../shared/ui/BackendError";
import { SuccessAlert } from "../../../shared/ui/Alerts";
import { FaArrowLeftLong } from "react-icons/fa6";
import { extendedFormElements } from "../../../shared/types/extendedForm";
import { useAppDispatсh, useAppSelector } from "../../../shared/store";

export const Auth = () => {
    const { authType } = useParams<{authType: string}>()
    const navigate = useNavigate()
    
    const dispatch = useAppDispatсh()
    const authError = useAppSelector(selectAuthError)
    const currentUser = useAppSelector(selectCurrentUser)
    //hook for handling login and register
    const { handleLoginAndRegister, isLoginSuccess, isRegisterSuccess } = useHandleLoginAndRegister()
    
    return (
        <section className="bg-gray-50 dark:bg-gray-900 relative">
            <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
                {
                isLoginSuccess &&
                <div className="flex gap-3 flex-col">
                    <SuccessAlert mainText={'Вход выполнен'}/>
                    <div 
                    className="w-full text-center hover:cursor-pointer"
                    onClick={() => navigate(`/${currentUser?.role_type}/variants`, {replace: true})}>
                        Перейти к главной странице
                    </div>
                </div>
                }
                {
                    isRegisterSuccess &&
                    <div className="flex flex-col gap-3">
                        <SuccessAlert mainText={'Регистрация выполнена'}/>
                        <div
                        className="w-full text-center hover:cursor-pointer" 
                        onClick={() => navigate('/login')}>
                            Перейти ко входу
                            </div>
                    </div>
                }
                 { !isLoginSuccess && !isRegisterSuccess &&
                <div className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
                    <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
                        <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                            {authType === 'login' ? 'Вход в аккаунт' : 'Регистрация'}
                        </h1>
                        <form className="space-y-4 md:space-y-6" onSubmit={(e: FormEvent<extendedFormElements>) => handleLoginAndRegister(e, authType)}>
                            <div>
                                <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Ваш логин</label>
                                <input 
                                onFocus={() => dispatch(setAuthError(null))} 
                                type="text" 
                                name="email" 
                                id="email" 
                                className="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="login" required={true}/>
                            </div>
                            <div>
                                <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Ваш пароль</label>
                                <input 
                                onFocus={() => setAuthError(null)} 
                                type="password" 
                                name="password" 
                                id="password" 
                                placeholder="••••••••" 
                                className="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required={true}/>
                            </div>
                            
                            <button type="submit" className="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">
                                {authType === 'login' ? 'Войти' : 'Зарегистрироваться'}
                            </button>
                            <div className="text-sm font-light text-gray-500 dark:text-gray-400 flex flex-row gap-2">
                                {authType === 'login' ? 'Еще нет аккаунта? ' : 'Уже есть аккаунт? '}
                                <a href="#" className="font-medium text-primary-600 hover:underline dark:text-primary-500" onClick={() => navigate(`/auth/${authType === 'login' ? 'register' : 'login'}`)}>
                                    {authType === 'login' ? 'Зарегистрироваться' : 'Войти'}                                          
                                </a>
                            </div>
                        </form>
                    </div>
                </div>
                }
                {authError && <BackendError error={authError} />}
            </div>
        </section>
    )
}