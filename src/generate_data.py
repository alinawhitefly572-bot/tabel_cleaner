import random
from itertools import product
from pathlib import Path

import pandas as pd

#random.seed(42)

#Оси для будущей таблицы

family_name = ['Иванов', 'Петров', 'Сидоров', 'Потапов', 'Хомяков', 'Горбушин', 'Павлов','Голубев','Солдатов','Кузнецов']
first_name = ['Виктор', 'Андрей', 'Рауль', 'Сергей', 'Федор', 'Дмитрий', 'Данил', 'Константин', 'Владимир', 'Михаил']
patronymic = ['Александрович', 'Михаилыч', 'Степанович', 'Владимирович', 'Евгеньевич', 'Рустамович', 'Максимович', 'Константинович', 'Владиславович', 'Николаевич']
Email_1 = ['Usup','dhjk','dsg','dsg','rgdsg','asdg','gadsg','gfd','fdhs','kjlh']
Email_2 = ['ldpr', 'ussr', 'mvd', 'gulag', 'terminator', 'deepseek','cotofox','emperium','kista','lain']
sity = ['Екатеринбург', 'Челябинск','Уфа','Копейск','Магнитогорск','Златоуст','Сатка','Касли','Иерусалим','Владивосток']
DOMAINS = ['gmail.com', 'mail.ru', 'yandex.ru', 'bk.ru', 'list.ru', 'inbox.ru', 'gmail.com', 'mail.ru', 'yandex.ru', 'gmail.com']

rows = []

def corrupt_phone(phone: str) -> str:
    """Портит формат телефона, как в реальных базах."""
    digits = ''.join(c for c in phone if c.isdigit())
    variant = random.choice([1, 2, 3, 4, 5])
    if variant == 1:
        return phone                                          # как есть
    if variant == 2:
        return digits                                         # 89995904099
    if variant == 3:
        return f"8 {digits[1:4]} {digits[4:7]} {digits[7:9]} {digits[9:]}"  # 8 999 590 40 99
    if variant == 4:
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:]}"  # +7 (999) 590-40-99
    return f"+7-{digits[1:4]}-{digits[4:7]}-{digits[7:9]}-{digits[9:]}"  # +7-999-590-40-99

def corrupt_email(email: str) -> str:
    """Разный регистр, пробелы, опечатки."""
    variant = random.choice([1, 2, 3, 4])
    if variant == 1:
        return email
    if variant == 2:
        return email.upper()
    if variant == 3:
        return f" {email} "                    # пробелы по краям
    return email.replace('@', ' @')            # пробел перед @

#Генерация данных
def ganerate_data():
    for i in range(100):
        a = random.randint(0, 9)
        b = random.randint(0, 9)
        c = random.randint(0, 9)
        FIO = f'{family_name[a]} {first_name[b]} {patronymic[c]}'
        phone_number = f'+79456{9-a}{9-b}{9-c}{a}{b}{c}'
        Email = f'{Email_1[a]}{Email_2[b]}{c}@{DOMAINS[b]}'
        date = f'{random.randint(1, 28)}.{random.randint(1, 12)}.201{a}'
        rows.append({
            'ФИО': FIO,
            'Телефон': corrupt_phone(phone_number),
            'Email': corrupt_email(Email),
            'Город': sity[a],
            'Дата обращения': date,

        })
    df = pd.DataFrame(rows)
    return(df)

#print(ganerate_data())

output_dir = Path(__file__).parent.parent / 'examples'
output_dir.mkdir(parents=True, exist_ok=True)

ganerate_data().to_excel(output_dir / 'people.xlsx', index=False)
print(f'Сохранено: {output_dir / "people.xlsx"}')
#for fam, fst, pat in product(family_name, first_name, patronymic):
 #   print(f'{fam} {fst} {pat}')