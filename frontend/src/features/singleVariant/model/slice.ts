import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// Define the type for the state
interface MyState {
    variantAnswers: { [key: string]: string  }; // Object with string keys and string values
}

// Initial state
const initialState: MyState = {
    variantAnswers: {}, // Empty object
};

// Create the slice
export const variantAnswersSlice = createSlice({
    name: 'answersToVariant',
    initialState,
    reducers: {
        // Action to add a key-value pair to the object
        addAnswerToTask: (state, action: PayloadAction<{ task_id: string | undefined; answer: string }>) => {
            const { task_id, answer } = action.payload;
            if (!task_id) {
                return;
            }
            state.variantAnswers[task_id] = answer;
        },
    },
    selectors: {
        // Selector to get the entire object
        selectAnswerToTask: (state, task_id: string | undefined) => {
            if (!task_id) {
                return 
            }
            if (task_id in state.variantAnswers) {
                return state.variantAnswers[task_id]
            } else{
                return ''
            }
        },
        selectVariantAnswers: (state) => state.variantAnswers,
    }
});

// Export the action
export const { addAnswerToTask } = variantAnswersSlice.actions;
export const { selectVariantAnswers, selectAnswerToTask } = variantAnswersSlice.selectors;
// Selector to get the entire object

