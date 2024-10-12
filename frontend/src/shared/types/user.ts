// TODO переписать subject на отдельный тип subject вместо string

export type userCreate = {
    email: string,
    password: string
}

export type userRead = {
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