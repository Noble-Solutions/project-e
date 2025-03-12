import { selectCurrentUser } from "../entities/user/model/user.slice";
import { useAppSelector } from "../shared/store";
import { Link, useParams } from "react-router-dom";
import { VscAccount } from "react-icons/vsc";
import { useHandleLogout } from "../pages/auth/utils/logout";
export const Header = () => {
    const params = useParams()
    const currentUser = useAppSelector(selectCurrentUser)
    const { handleLogout } = useHandleLogout();
    console.log(JSON.stringify(params))
    return (
        <>
        <header className="shadow">
            <nav className="bg-white border-gray-200 lg:w-[84%] mx-auto py-2.5 dark:bg-gray-800">
                <div className="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl">
                    <div className="flex items-center gap-3">
                        <VscAccount className="text-3xl"/>
                        <span>
                            {
                                currentUser ? `${currentUser.last_name} ${currentUser.first_name[0]}.` : 'Гость'
                            }
                        </span>
                    </div>
                    {
                        currentUser &&
                        <>
                            <div className="flex items-center justify-center">
                                <Link to={`/${currentUser?.role_type}/variants/list`}>
                                    Варианты
                                </Link>
                            </div>
                            {
                            currentUser.role_type === 'teacher' &&
                            <>
                                <div className="flex items-center justify-center">
                                    <Link to={`/${currentUser?.role_type}/classes/list`}>
                                        Классы
                                    </Link>
                                </div>
                                <div className="flex items-center justify-center">
                                    <Link to={`/teacher/tasks/list`}>
                                        Задания
                                    </Link>
                                </div>
                            </>
                            }
                        </>
                    }
                    <div className="flex items-center lg:order-2">
                        {
                        currentUser === null ?
                        <>
                            <Link to='/auth/login' className="text-gray-800 dark:text-white bg-gray-100 ring-4ring-gray-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 dark:hover:bg-gray-700 focus:outline-none dark:focus:ring-gray-800">Вход</Link>
                            <Link to='/auth/register' className="text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 dark:bg-primary-600 dark:hover:bg-primary-700 focus:outline-none dark:focus:ring-primary-800">Регистрация</Link>
                        </>
                        : 
                        <button
                        onClick={handleLogout}
                        className="text-gray-800 dark:text-white bg-gray-100 ring-4ring-gray-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 dark:hover:bg-gray-700 focus:outline-none dark:focus:ring-gray-800">
                            Выход
                        </button>
                        }
                    </div>
                </div>
            </nav>
        </header>
        </>
    )
}






