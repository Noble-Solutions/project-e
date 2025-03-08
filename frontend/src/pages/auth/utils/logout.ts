import { useAppDispatсh } from "../../../shared/store";
import { useLogoutMutation } from "../api/api";
import { logOut } from "../../../entities/user/model/user.slice";

export const useHandleLogout = () => {
    const dispatch = useAppDispatсh();
    const [logoutRequest] = useLogoutMutation();

    /**
     * Обрабатывает выход пользователя из системы.
     * Отправляет запрос на логаут, удаляет токены из cookies
     * и обновляет состояние пользователя в Redux.
     *
     * @return {Promise<void>} A promise that resolves when the logout is complete
     */
    const handleLogout = async (): Promise<void> => {
        try {
            // Отправляем запрос на логаут
            await logoutRequest().unwrap();

            // Очищаем состояние пользователя в Redux
            dispatch(logOut());
        } catch (err) {
            console.error("Ошибка при выходе из системы:", err);
        }
    };

    return { handleLogout };
};
