import { Outlet } from "react-router-dom"

/**
 * Компонент обертка, позволяющий переключаться между "VariantsList" и
 * "VariantCreate"
 */
export const Variants = () => {
    return (
        <Outlet />
    )
}