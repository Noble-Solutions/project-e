import { Outlet } from "react-router-dom"

/**
Компонент обертка, позволяющий переключаться между "ClassroomsList" и 
"ClassroomCreate"
*/
export const Classrooms = () => {
    return (
        <Outlet />
    )
}