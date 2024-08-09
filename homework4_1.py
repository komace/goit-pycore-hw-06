from collections import UserDict
import re
# створюємо клас для управління адресною книгою
class Field:
    def __init__(self, value):
        self.value = value
    # метод перетворює обєкт класу у рядок 
    def __str__(self):
        return str(self.value)

# клас призначений для зберігання імені контакту
class Name(Field):
    def __init__(self, value):
        super().__init__(value)


# клас призначений для зберігання номеру телефону
class Phone(Field):
    def __init__(self, value):
        self._validate_phone(value)
        super().__init__(value)
    # перевірка чи введено 10 значний номер телефону за допомогою регулярного виразу
    def _validate_phone(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must be exactly 10 digits")


# Клас призначений для зберігання та управління інформацією про контакт
class Record:
    # зберігає імя контакту в порожній список - self.phones = []
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    # додає новий номер телефону до списку
    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)
    # перебирає всі телефони у списку та видаляє номер телефону який буде переданий
    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break
    # редагує існуючий телефон замінюючи на новий
    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                break
    # знаходить і повертає об'єкт з номером
    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    # повертає рядкове представлення об'єкта
    def __str__(self):
        phones = '; '.join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"

# створенмо клас для управління колекцією контактів
class AddressBook(UserDict):

    # додає новий контактний запис до адресної книги.
    def add_record(self, record):
        self.data[record.name.value] = record
    # знаходить і повертає запис контакту за його ім'ям
    def find(self, name):
        return self.data.get(name)
    # видаляє запис контакту за його ім'ям
    def delete(self, name):
        if name in self.data:
            del self.data[name]


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
