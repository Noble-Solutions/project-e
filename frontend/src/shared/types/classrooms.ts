import { teacherRead } from "./user"
//TODO протипизровать id как UUID вместо строки если будет необходимо
export type classroomCreate = {
    name: string,
    subject: string
}

export type classroomRead = classroomCreate & {
    id: string,
    amount_of_students: number
}

type classroomFromDB = {
    classroom_data: classroomRead,
    teacher?: teacherRead
}

export type classroomListFromDB = {
    classrooms: classroomFromDB[]
}
