import pandas as pd

def remove_empty_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    before = len(df)
    df = df.dropna(how='all')
    df = df[~df.apply(lambda row: row.astype(str).str.strip().eq('').all(), axis=1)]
    removed = before - len(df)
    return df, removed

def remove_useless_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    # Удаляет строки, где нет ни ФИО, ни Телефоона (бесполезные записи, по которым нельзя определить клиента)
    before = len(df)
    if 'ФИО' in df.columns and 'Телефон' in df.columns:
        mask = (df['ФИО'].astype(str).str.strip() != '') | (df['Телефон'].astype(str).str.strip() != "")
        df = df[mask]
    removed = before - len(df)
    return df, removed

def strip_spaces(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()
    return df

def fill_empty(df: pd.DataFrame) -> pd.DataFrame:
    return df.fillna('Не указано')

def clean_dataframe(df: pd.DataFrame) -> dict:
    df = df.copy()
    total_before = len(df)

    #
    df = strip_spaces(df)

    #
    df, removed_empty = remove_empty_rows(df)

    #
    df, removed_useless = remove_useless_rows(df)

    #
    df = fill_empty(df)

    df = df.reset_index(drop=True)

    return {
        'data': df,
        'before': total_before,
        'after': len(df),
        'removed_empty': removed_empty,
        'removed_useless': removed_useless,
        'total_removed': total_before - len(df),
    }
"""
if __name__ == '__main__':
    # Быстрый тест на маленьком DataFrame
    test_df = pd.DataFrame({
        'ФИО': ['  Иванов  ', '', 'Петров', '   '],
        'Телефон': ['+79991234567', '', '', '  '],
        'Email': ['ivanov@mail.ru', None, 'petrov@mail.ru', ''],
    })

    print('До очистки:')
    print(test_df)
    print()

    result = clean_dataframe(test_df)

    print('После очистки:')
    print(result['data'])
    print()
    print(f"Удалено пустых строк: {result['removed_empty']}")
    print(f"Удалено бесполезных:  {result['removed_useless']}")
    print(f"Всего удалено:        {result['total_removed']}")
"""