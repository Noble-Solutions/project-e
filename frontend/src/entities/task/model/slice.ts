import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { TaskCreate } from "../types/types";

const initialState: TaskCreate = {
    type: 0,
    text: '',
    type_of_answer: 'full_answer',
    correct_answer: undefined,
}

export const taskFormFieldsSlice = createSlice({
    name: 'taskFormFields',
    initialState,
    reducers: {
        setFormData(state, action: PayloadAction<Partial<TaskCreate>>) {
            return { ...state, ...action.payload };
          },
        resetForm() {
        return initialState;
        },
    },
    selectors: {
        selectFormData(state) {
            return state
        }
    }
})

export const { setFormData, resetForm } = taskFormFieldsSlice.actions
export const { selectFormData } = taskFormFieldsSlice.selectors