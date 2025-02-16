// TODO переписать subject на отдельный тип subject вместо string

export type userCreate = {
    username: string,
    password: string,
    first_name: string,
    last_name: string
    role_type: string,
    subject: string | null
}

export type userRead = {
    id: string,
    username: string,
    role_type: "teacher" | "student",
    first_name: string,
    last_name: string
}

export type teacherRead = userRead & {
    subject?: string,
}

export type studentRead = userRead & {

}