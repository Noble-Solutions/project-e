import { RefObject } from "react";

export const manualFormSubmitTrigger =  (formRef: RefObject<HTMLFormElement>) => {
    if (formRef.current) {
        formRef.current.dispatchEvent(new Event('submit', { bubbles: true }));
    }
}