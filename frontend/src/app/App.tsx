import { useEffect } from "react"
import { Outlet, useLocation, useNavigate } from "react-router-dom"

export const App = () => {
    const { pathname } = useLocation()
    const navigate = useNavigate()
    useEffect(() => {
        if (pathname.substring(1) === '') {
            navigate('auth/login/')
        }
    }, [])
    return (
        <Outlet />
    )
}

