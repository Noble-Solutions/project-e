import { useParams } from "react-router-dom";
import { studentRead } from "../../../shared/types/user"
import { MdDelete } from "react-icons/md";
import { useRemoveStudentFromClassroomMutation } from "../api/api";
export const StudentCard = ({student}: {student: studentRead}) => {
    const [deleteStudentFromClassroom] = useRemoveStudentFromClassroomMutation()
    const id = useParams<string>()
    const handleDeleteStudentButtonClick = async () => {
        try {
            if (!id.id) {
                return
            }
            await deleteStudentFromClassroom({student_id: student.id, classroom_id: id.id}).unwrap()
            .then((data) => {
                console.log(data)
                
            })
        }  catch (err: any) {
                if ('data' in err && 'status' in err) {
                    console.log(err.data)
                } else {
                    console.log(err)
                }
            }
    }
    return (
        <li className="group flex flex-row justify-between items-center p-2 border-black border-opacity-20 border-2 rounded-lg shadow-md" key={student.id}>
            <p className="transition-all duration-1000 ease-in-out group-hover:underline">
                {student.first_name} {student.last_name}
            </p>
            <MdDelete onClick={handleDeleteStudentButtonClick}/>
        </li>
    );
}


