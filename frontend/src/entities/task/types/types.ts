export type TaskCreate = {
    text: string,
    type: number,
    type_of_answer: "full_answer" | "short_answer",
    correct_answer?: string,
}

export type TaskRead = TaskCreate & {
    id: string,
    file_id: string,
    file_extension: string,
    teacher_id: string,
}