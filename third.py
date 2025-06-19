import csv
from datetime import datetime

FILENAME = 'data.csv'

def read_data(filename):
    """Считывает данные из CSV в список словарей."""
    with open(filename, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    # Преобразуем числовые поля к нужным типам
    for row in data:
        row['№'] = int(row['№'])
        row['размер стипендии'] = float(row['размер стипендии'])
        # Можно преобразовать дату в datetime, если нужно
        # row['дата'] = datetime.strptime(row['дата'], '%Y-%m-%d')
    return data

def print_data(data):
    """Выводит данные в табличном виде."""
    print(f"{'№':<3} {'Дата':<12} {'ФИО студента':<25} {'Стипендия':<10} {'Куда выдается'}")
    print('-' * 70)
    for d in data:
        print(f"{d['№']:<3} {d['дата']:<12} {d['ФИО студента']:<25} {d['размер стипендии']:<10} {d['куда выдается справка']}")

def sort_by_string_field(data, field):
    """Сортирует по строковому полю."""
    return sorted(data, key=lambda x: x[field].lower())

def sort_by_numeric_field(data, field):
    """Сортирует по числовому полю."""
    return sorted(data, key=lambda x: x[field])

def filter_by_scholarship(data, min_amount):
    """Фильтрует записи, где размер стипендии больше min_amount."""
    return [d for d in data if d['размер стипендии'] > min_amount]

def add_record(data):
    """Добавляет новую запись, запрашивая данные у пользователя."""
    print("Добавление новой справки:")
    try:
        no = max(d['№'] for d in data) + 1
    except ValueError:
        no = 1
    date = input("Введите дату (YYYY-MM-DD): ")
    fio = input("Введите ФИО студента: ")
    stipend = float(input("Введите размер стипендии: "))
    place = input("Куда выдается справка: ")
    new_record = {
        '№': no,
        'дата': date,
        'ФИО студента': fio,
        'размер стипендии': stipend,
        'куда выдается справка': place
    }
    data.append(new_record)
    print("Запись добавлена.")

def save_data(filename, data):
    """Сохраняет данные обратно в CSV."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['№', 'дата', 'ФИО студента', 'размер стипендии', 'куда выдается справка']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for d in data:
            # Преобразуем числовые поля обратно в строки для записи
            row = {
                '№': str(d['№']),
                'дата': d['дата'],
                'ФИО студента': d['ФИО студента'],
                'размер стипендии': str(d['размер стипендии']),
                'куда выдается справка': d['куда выдается справка']
            }
            writer.writerow(row)
    print(f"Данные сохранены в файл {filename}")

def main():
    data = read_data(FILENAME)
    print("Исходные данные:")
    print_data(data)

    # Сортировка по строковому полю (например, по ФИО)
    print("\nСортировка по ФИО студента:")
    sorted_by_name = sort_by_string_field(data, 'ФИО студента')
    print_data(sorted_by_name)

    #oeiropweireopwr

    #feature11111

    # Сортировка по числовому полю (например, по размеру стипендии)
    print("\nСортировка по размеру стипендии:")
    sorted_by_stipend = sort_by_numeric_field(data, 'размер стипендии')
    print_data(sorted_by_stipend)

    # Фильтрация по критерию (размер стипендии > 1500)
    print("\nСтуденты с размером стипендии больше 1500:")
    filtered = filter_by_scholarship(data, 1500)
    print_data(filtered)

    # Добавление новой записи
    add_record(data)

    # Сохраняем данные обратно в файл
    save_data(FILENAME, data)

if __name__ == '__main__':
    main()

