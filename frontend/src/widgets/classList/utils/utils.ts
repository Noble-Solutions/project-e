export const formatName = (name: string): string => {
    // Разделяем имя на части
    const parts = name.trim().split(' ');

    // Получаем первую букву первого имени и добавляем точку
    const firstInitial = parts[0].charAt(0).toUpperCase() + '.';

    // Получаем фамилию (предполагаем, что она последняя)
    const lastName = parts[parts.length - 1].charAt(0).toUpperCase() + parts[parts.length - 1].slice(1).toLowerCase();

    // Возвращаем отформатированное имя
    return `${firstInitial} ${lastName}`;
}