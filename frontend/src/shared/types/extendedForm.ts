export interface extendedFormElements extends HTMLFormElement{
    elements: formElements
}

interface formElements extends HTMLFormControlsCollection {
    [index: number]: HTMLInputElement & { value?: unknown };
}