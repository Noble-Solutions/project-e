import { useState } from "react";
import { Link } from "react-router-dom";


export const AddTaskDropdown = ({id}: {id: string | undefined}) => {
     const [isOpen, setIsOpen] = useState(false); // State to manage dropdown visibility
    
        // Toggle dropdown visibility
        const toggleDropdown = () => {
            setIsOpen(!isOpen);
        };
    
        // Close dropdown when an option is selected
        const handleOptionClick = () => {
            setIsOpen(false);
        };
    return (
        <div>
            {/* Dropdown Button */}
            <button
                id="dropdownDefaultButton"
                onClick={toggleDropdown}
                className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                type="button"
            >
                Добавить задание
                <svg
                    className="w-2.5 h-2.5 ms-3"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 10 6"
                >
                    <path
                        stroke="currentColor"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="m1 1 4 4 4-4"
                    />
                </svg>
            </button>

            {/* Dropdown Menu */}
            {isOpen && (
                <div
                    id="dropdown"
                    className="z-10 absolute bg-white divide-y divide-gray-100 rounded-lg shadow-sm w-44 dark:bg-gray-700"
                >
                    <ul
                    className="py-2 text-sm text-gray-700 dark:text-gray-200"
                    aria-labelledby="dropdownDefaultButton"
                    >
                        <li>
                            <Link
                                to={`../../../tasks/list/${id}`}
                                className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
                                onClick={handleOptionClick}
                            >
                                Выбрать из банка заданий
                            </Link>
                        </li>
                        <li>
                            <Link
                                to={`../../../tasks/create/${id}`}
                                className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
                                onClick={handleOptionClick}
                            >
                                Создать новое
                            </Link>
                        </li>
                        {/* <li>
                            <Link
                                to="/earnings"
                                className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
                                onClick={handleOptionClick}
                            >
                                Импортировать из Экселя
                            </Link>
                        </li> */}
                    </ul>
                </div>
            )}
        </div>
    )
}


