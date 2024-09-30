export type UserCreate = {
    email: string,
    password: string
}

export type userRead = {
    username: string,
    role_type: "teacher" | "student"
}