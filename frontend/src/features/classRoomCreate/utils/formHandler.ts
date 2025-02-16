import { FormEvent } from "react"
import { useCreateClassroomMutation } from "../api/api"
import { extendedFormElements } from "../../../shared/types/extendedForm"
import { classroomCreate } from "../../../shared/types/classrooms"

export const useHandleCreateClassroom = () => {
    const [createClassroom, { isSuccess: isCreateCLassroomSuccess }] = useCreateClassroomMutation()
    const handleCreateClassroom = async (e: FormEvent<extendedFormElements>): Promise<void> => {
        e.preventDefault()
        const { elements } = e.currentTarget
        const name = elements[0].value
        const classroomCreateData: classroomCreate = {
            name
        }
        try {
            console.log(classroomCreateData)
            await createClassroom(classroomCreateData).unwrap()
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
        return { handleCreateClassroom, isCreateCLassroomSuccess }
    }