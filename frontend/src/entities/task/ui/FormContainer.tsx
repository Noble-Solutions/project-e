export const FormContainer = ({formElement, secondFormElement}: {formElement: React.ReactNode, secondFormElement?: React.ReactNode}) => {
    return (
        <section className="bg-white dark:bg-gray-900">
            <div className="py-8 px-4 mx-auto max-w-2xl lg:py-16">
                <h2 className="mb-4 text-xl font-bold text-gray-900 dark:text-white">Добавить новое задание</h2>
                {formElement}
                {secondFormElement && secondFormElement}
            </div>
        </section>
    )
}


