type AlertProps = {
    mainText: string,
    optionalText?: string
}
export const SuccessAlert = ({mainText, optionalText}: AlertProps) => {
    return (
        <div className="flex items-center p-4 mt-4 text-sm text-green-800 border border-green-300 rounded-lg bg-green-50 dark:bg-gray-800 dark:text-green-400 dark:border-green-800" role="alert">
            <div>
                <span className="font-medium">{mainText}</span> {optionalText}
            </div>
        </div>
    )
}

export const WarningAlert = ({mainText, optionalText}: AlertProps) => {
    return (
        <div className="flex items-center p-4 mt-4 text-sm text-yellow-800 border border-yellow-300 rounded-lg bg-yellow-50 dark:bg-gray-800 dark:text-green-400 dark:border-green-800" role="alert">
            <div>
                <span className="font-medium">{mainText}</span> {optionalText}
            </div>
        </div>
    )
}