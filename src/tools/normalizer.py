"""
Модуль нормализации CRM-данных.

Приводит телефон, email и ФИО к единому формату,
чтобы потом можно было корректно искать дубликаты.
"""
import re

import pandas as pd


# ============================================================
# ФУНКЦИИ НОРМАЛИЗАЦИИ (работают с одной ячейкой)
# ============================================================

def normalize_phone(phone) -> str:
    """
    Приводит любой телефон к формату +7XXXXXXXXXX.
    
    Примеры:
        '+7 (945) 623-17-68'  → '+79456231768'
        '8 945 667 83 21'     → '+79456678321'
        '79456509490'         → '+79456509490'
    """
    if pd.isna(phone):
        return ''
    digits = re.sub(r'\D', '', str(phone))
    if len(digits) == 11 and digits[0] in ('7', '8'):
        return '+7' + digits[1:]
    return digits


def normalize_email(email) -> str:
    """
    Email → нижний регистр без пробелов.
    
    Примеры:
        'RGDSGLAIN0@GMAIL.COM'  → 'rgdsglain0@gmail.com'
        'gadsggulag9 @bk.ru'    → 'gadsggulag9@bk.ru'
    """
    if pd.isna(email):
        return ''
    return str(email).replace(' ', '').lower()


def normalize_name(name) -> str:
    """
    ФИО → без лишних пробелов, каждое слово с большой буквы.
    
    Примеры:
        '  Иванов   Иван  '     → 'Иванов Иван'
        'иванов иван иванович'  → 'Иванов Иван Иванович'
    """
    if pd.isna(name):
        return ''
    cleaned = ' '.join(str(name).split())
    return cleaned.title()


def normalize_city(city) -> str:
    """
    Город → без пробелов, первая буква заглавная.
    
    Примеры:
        'москва'     → 'Москва'
        ' Магнитогорск '  → 'Магнитогорск'
    """
    if pd.isna(city):
        return ''
    return str(city).strip().title()


# ============================================================
# ФУНКЦИЯ ДЛЯ ВСЕЙ ТАБЛИЦЫ
# ============================================================

def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Нормализует все поддерживаемые столбцы в DataFrame.
    
    Ищет столбцы по названию и применяет нужную функцию.
    Если столбца нет — пропускает.
    """
    df = df.copy()  # не мутируем исходный
    
    column_map = {
        'Телефон': normalize_phone,
        'Email': normalize_email,
        'ФИО': normalize_name,
        'Город': normalize_city,
    }
    
    for col, func in column_map.items():
        if col in df.columns:
            df[col] = df[col].apply(func)
    
    return df


# ============================================================
# ПРОВЕРКА (запуск напрямую)
# ============================================================
if __name__ == '__main__':
    test_emails = [
        'usupemperium6 @mail.ru',
        '  IVANOV@MAIL.RU  ',
        'gadsggulag9@bk.ru',
        '\tDSGMVD1@YANDEX.RU\n',
    ]
    print('Проверка email:')
    for e in test_emails:
        print(f'  {e!r:35} → {normalize_email(e)!r}')