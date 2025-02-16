import { studentRead, teacherRead } from "./user"
//TODO протипизровать id как UUID вместо строки если будет необходимо

// TODO поработать с этими типами ужасными
export type classroomCreate = {
    name: string,
}

export type classroomRead = classroomCreate & {
    subject: string,
    id: string,
    amount_of_students: number
}

type classroomFromDB = {
    classroom_data: classroomRead,
    teacher?: teacherRead
}

export type clasroomWithStudentsAndTeacher = {
    classroom_data: classroomRead,
    students: studentRead[]
    teacher: teacherRead
}

export type classroomListFromDB = {
    classrooms: classroomFromDB[]
}
