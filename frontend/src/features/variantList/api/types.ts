export type VariantRead = {
    id: string;
    name: string;
    subject: string;
    amount_of_tasks: number;
    maximum_score_from_short_answer_task: number;
    teacher_id: string;
};

export type VariantList = {
    variants: VariantRead[];
};

