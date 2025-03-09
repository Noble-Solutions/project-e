import { Outlet } from "react-router-dom"
import { Header } from "../../../widgets/header"
import { selectCurrentUser } from "../../../entities/user/model/user.slice"
import { useNavigate } from "react-router-dom"
import { useAppSelector } from "../../../shared/store"
import { useEffect } from "react"
export const Root = () => {
    const navigate = useNavigate()
    const user = useAppSelector(selectCurrentUser)
    useEffect(() => {
        if (!user) {
            navigate('/auth/login')
        }
    }, [user])
    return (
        <>
            <Header />
            <Outlet />
        </>
    )
}


