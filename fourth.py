import csv
from datetime import datetime
from typing import Iterator, List, Optional

FILENAME = 'data.csv'


class Scholarship:
    """Класс для представления справки о стипендии."""

    def __init__(self, number: int, date: str, student_name: str, amount: float, destination: str):
        # Используем __setattr__ для установки значений
        self.__setattr__('_number', number)
        self.__setattr__('_date', date)
        self.__setattr__('_student_name', student_name)
        self.__setattr__('_amount', amount)
        self.__setattr__('_destination', destination)

    def __setattr__(self, name: str, value):
        """Перегрузка установки атрибутов с валидацией."""
        if name == '_number' and not isinstance(value, int):
            raise ValueError("Номер должен быть целым числом")
        elif name == '_amount' and not isinstance(value, (int, float)):
            raise ValueError("Размер стипендии должен быть числом")
        elif name in ['_date', '_student_name', '_destination'] and not isinstance(value, str):
            raise ValueError("Строковые поля должны быть строками")
        super().__setattr__(name, value)

    def __repr__(self) -> str:
        """Строковое представление объекта."""
        return f"Scholarship(№{self._number}, {self._student_name}, {self._amount})"

    def __str__(self) -> str:
        """Пользовательское строковое представление."""
        return f"{self._number:<3} {self._date:<12} {self._student_name:<25} {self._amount:<10} {self._destination}"

    # Свойства для доступа к полям
    @property
    def number(self) -> int:
        return self._number

    @property
    def date(self) -> str:
        return self._date

    @property
    def student_name(self) -> str:
        return self._student_name

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def destination(self) -> str:
        return self._destination

    @staticmethod
    def validate_date(date_str: str) -> bool:
        """Статический метод для валидации даты."""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    @staticmethod
    def format_amount(amount: float) -> str:
        """Статический метод для форматирования суммы."""
        return f"{amount:.2f} руб."


class HighScholarship(Scholarship):
    """Наследуемый класс для высоких стипендий (наследование)."""

    def __init__(self, number: int, date: str, student_name: str, amount: float, destination: str, bonus: float = 0):
        super().__init__(number, date, student_name, amount, destination)
        self.__setattr__('_bonus', bonus)

    @property
    def bonus(self) -> float:
        return self._bonus

    @property
    def total_amount(self) -> float:
        """Общая сумма с бонусом."""
        return self._amount + self._bonus

    def __repr__(self) -> str:
        return f"HighScholarship(№{self._number}, {self._student_name}, {self.total_amount})"


class ScholarshipCollection:
    """Класс для работы с коллекцией справок о стипендиях."""

    def __init__(self):
        self._scholarships: List[Scholarship] = []

    def __iter__(self) -> Iterator[Scholarship]:
        """Итератор для коллекции."""
        return iter(self._scholarships)

    def __getitem__(self, index: int) -> Scholarship:
        """Доступ к элементам по индексу."""
        return self._scholarships[index]

    def __len__(self) -> int:
        """Длина коллекции."""
        return len(self._scholarships)

    def __repr__(self) -> str:
        """Строковое представление коллекции."""
        return f"ScholarshipCollection({len(self._scholarships)} items)"

    def add_scholarship(self, scholarship: Scholarship):
        """Добавление справки в коллекцию."""
        self._scholarships.append(scholarship)

    def remove_scholarship(self, index: int):
        """Удаление справки по индексу."""
        if 0 <= index < len(self._scholarships):
            del self._scholarships[index]

    def filter_by_amount(self, min_amount: float):
        """Генератор для фильтрации по размеру стипендии."""
        for scholarship in self._scholarships:
            if scholarship.amount > min_amount:
                yield scholarship

    def sort_by_name_generator(self):
        """Генератор для сортировки по имени."""
        sorted_scholarships = sorted(self._scholarships, key=lambda x: x.student_name.lower())
        for scholarship in sorted_scholarships:
            yield scholarship

    def sort_by_amount_generator(self):
        """Генератор для сортировки по размеру стипендии."""
        sorted_scholarships = sorted(self._scholarships, key=lambda x: x.amount)
        for scholarship in sorted_scholarships:
            yield scholarship

    def get_high_scholarships_generator(self, threshold: float = 2000):
        """Генератор высоких стипендий."""
        for scholarship in self._scholarships:
            if scholarship.amount > threshold:
                # Создаем объект высокой стипендии
                yield HighScholarship(
                    scholarship.number,
                    scholarship.date,
                    scholarship.student_name,
                    scholarship.amount,
                    scholarship.destination,
                    scholarship.amount * 0.1  # 10% бонус
                )

    @staticmethod
    def create_from_csv(filename: str) -> 'ScholarshipCollection':
        """Статический метод для создания коллекции из CSV файла."""
        collection = ScholarshipCollection()
        try:
            with open(filename, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    scholarship = Scholarship(
                        int(row['№']),
                        row['дата'],
                        row['ФИО студента'],
                        float(row['размер стипендии']),
                        row['куда выдается справка']
                    )
                    collection.add_scholarship(scholarship)
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
        return collection

    def save_to_csv(self, filename: str):
        """Сохранение коллекции в CSV файл."""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['№', 'дата', 'ФИО студента', 'размер стипендии', 'куда выдается справка']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for scholarship in self._scholarships:
                writer.writerow({
                    '№': scholarship.number,
                    'дата': scholarship.date,
                    'ФИО студента': scholarship.student_name,
                    'размер стипендии': scholarship.amount,
                    'куда выдается справка': scholarship.destination
                })

    def print_collection(self):
        """Вывод коллекции в табличном виде."""
        print(f"{'№':<3} {'Дата':<12} {'ФИО студента':<25} {'Стипендия':<10} {'Куда выдается'}")
        print('-' * 70)
        for scholarship in self._scholarships:
            print(scholarship)


def main():
    # Создаем коллекцию из CSV файла
    collection = ScholarshipCollection.create_from_csv(FILENAME)

    print("Исходные данные:")
    collection.print_collection()
    print(f"Представление коллекции: {repr(collection)}")

    # Демонстрация итератора
    print("\nИспользование итератора:")
    for i, scholarship in enumerate(collection):
        if i < 3:  # Показываем только первые 3
            print(f"  {repr(scholarship)}")

    # Демонстрация доступа по индексу
    print(f"\nПервый элемент коллекции: {collection[0]}")

    # Демонстрация генераторов
    print("\nСортировка по ФИО студента (генератор):")
    print(f"{'№':<3} {'Дата':<12} {'ФИО студента':<25} {'Стипендия':<10} {'Куда выдается'}")
    print('-' * 70)
    for scholarship in collection.sort_by_name_generator():
        print(scholarship)

    print("\nСортировка по размеру стипендии (генератор):")
    print(f"{'№':<3} {'Дата':<12} {'ФИО студента':<25} {'Стипендия':<10} {'Куда выдается'}")
    print('-' * 70)
    for scholarship in collection.sort_by_amount_generator():
        print(scholarship)

    # Фильтрация с помощью генератора
    print("\nСтуденты с размером стипендии больше 1500 (генератор):")
    print(f"{'№':<3} {'Дата':<12} {'ФИО студента':<25} {'Стипендия':<10} {'Куда выдается'}")
    print('-' * 70)
    for scholarship in collection.filter_by_amount(1500):
        print(scholarship)

    # Демонстрация наследования - высокие стипендии
    print("\nВысокие стипендии с бонусами (наследование + генератор):")
    for high_scholarship in collection.get_high_scholarships_generator(1800):
        print(f"{repr(high_scholarship)} - Общая сумма: {Scholarship.format_amount(high_scholarship.total_amount)}")

    # Демонстрация статических методов
    print(f"\nПроверка даты '2024-01-15': {Scholarship.validate_date('2024-01-15')}")
    print(f"Форматирование суммы 1500.5: {Scholarship.format_amount(1500.5)}")

    # Добавление новой записи
    print("\nДобавление новой справки:")
    try:
        max_number = max(s.number for s in collection) if len(collection) > 0 else 0
        new_scholarship = Scholarship(
            max_number + 1,
            "2024-01-15",
            "Новый Студент Студентович",
            2500.0,
            "Новое место"
        )
        collection.add_scholarship(new_scholarship)
        print(f"Добавлена запись: {repr(new_scholarship)}")
    except ValueError as e:
        print(f"Ошибка при создании записи: {e}")

    # Сохранение данных
    collection.save_to_csv(FILENAME)
    print(f"\nДанные сохранены в файл {FILENAME}")


if __name__ == '__main__':
    main()



# Итератор: Класс ScholarshipCollection реализует __iter__() для итерации по коллекции
# Перегрузка операций: Реализованы __repr__(), __str__(), __len__()
# Наследование: Класс HighScholarship наследуется от Scholarship
# setattr: Все установки значений проходят через __setattr__ с валидацией
# getitem: Реализован доступ к элементам коллекции по индексу
# Статические методы: validate_date(), format_amount(), create_from_csv()
# Генераторы: Несколько генераторов для сортировки, фильтрации и создания высоких стипендий