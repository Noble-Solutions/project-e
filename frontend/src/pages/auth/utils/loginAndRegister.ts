import { FormEvent } from "react"
import { extendedFormElements } from "../../../shared/types/extendedForm";
import { useAppDispatсh } from "../../../shared/store"
import { useLazyGetUserInfoQuery, useLoginMutation, useRegisterMutation,} from "../api/api"
import { setUser, setAuthError } from "../../../entities/user/model/user.slice"
import { userCreate } from "../../../shared/types/user";
import { FetchBaseQueryError } from "@reduxjs/toolkit/query";

export const useHandleLoginAndRegister = () => {
    const dispatch = useAppDispatсh()
    const [loginRequest, { isSuccess: isLoginSuccess }] = useLoginMutation()
    const [registerRequest, { isSuccess: isRegisterSuccess }] = useRegisterMutation()
    const [getUserInfoTriggerFunction] = useLazyGetUserInfoQuery()
    /**
     * Обрабатывает отправку форм как для входа, так и для регистрации.
     * Предотвращает отправку форм по умолчанию, извлекает данные формы
     * и отправляет запросы на вход или регистрацию на основе типа аутентификации.
     * Сбрасывает форму после успешной отправки и обрабатывает любые ошибки.    
     *
     * @param {FormEvent<extendedFormElements>} e - The form submission event
     * @return {Promise<void>} A promise that resolves when the submission is complete
     */
    const handleLoginAndRegister = async (e: FormEvent<extendedFormElements>, authType: string | undefined): Promise<void> => {
        e.preventDefault()
        
        const { elements } = e.currentTarget
        const login = elements[0].value
        const password = elements[1].value
        const form = e.currentTarget
        try {
            if (authType === 'login') {
                const loginFormData = new URLSearchParams({
                    'username' : login,
                    'password': password
                });
                console.log('made request')
                await loginRequest(loginFormData)
                await getUserInfoTriggerFunction().unwrap()
                .then((data) => {
                    console.log(data)
                    dispatch(setUser(data))
                })
            } else if (authType === 'register') {
                const firstName = elements[2].value
                const lastName = elements[3].value
                const roleType = elements[4].value
                let teacherSubject = null
                if (roleType === 'teacher') {
                    teacherSubject = elements[5].value
                }
                const registerFormData: userCreate = {
                    username: login,
                    password: password,
                    first_name: firstName, 
                    last_name: lastName,
                    role_type: roleType,
                    subject: teacherSubject
                }
                await registerRequest(registerFormData).unwrap()
            }
            form.reset()
        } catch (err: any) {
            if ('data' in err && 'status' in err) {
                console.log(err.data)
                dispatch(setAuthError(err as FetchBaseQueryError))
            } else {
                console.log(err)
            }
        }
    }
    
    return { handleLoginAndRegister, isLoginSuccess, isRegisterSuccess }
}