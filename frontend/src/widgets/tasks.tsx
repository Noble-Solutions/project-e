import { Outlet } from "react-router-dom"

/**
 * Компонент обертка, позволяющий переключаться между "TasksList" и
 * "TaskCreate"
 */
export const Tasks = () => {
    return (
        <Outlet />
    )
}