import { Link } from "react-router-dom"

export const List = () => {
    return (
        <div>
            <Link
            to="../create" 
            relative="path"
            >
                Создать задание
            </Link>
        </div>
    )
}