import { TaskRead } from "../../../entities/task"

type VariantRead = {
    id: string,
    name: string,
    subject: string,
    amount_of_tasks: number,
    teacher_id: string
}

export type getVariantByIdWithTasksResponse = {
    variant_data: VariantRead
    tasks: TaskRead[]
}

export type checkVariantResponse = {
    maximum_points: number,
    points_earned_by_student: number,
}