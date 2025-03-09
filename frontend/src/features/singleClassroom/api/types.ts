export type studentPerformanceResponse = {
    "task_stat": {
        "student_id": string,
        "classroom_id": string,
        "task_type": number,
        "correct_solved": number,
        "total_solved": number,
        "id": string
    }
}[]
