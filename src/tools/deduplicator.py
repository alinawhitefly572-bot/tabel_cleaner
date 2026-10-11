"""
Модуль удаления дубликатов из CRM-таблицы.
"""
from pathlib import Path

import pandas as pd

from .normalizer import normalize_dataframe   # ← точка!


def find_duplicates(df: pd.DataFrame, subset: list = None) -> tuple:
    """Возвращает (df_clean, df_dups)."""
    if subset is None:
        subset = ['Телефон', 'Email']
    
    df = df.copy()
    df['_is_dup'] = df.duplicated(subset=subset, keep='first')
    
    df_clean = df[~df['_is_dup']].drop(columns='_is_dup').reset_index(drop=True)
    df_dups = df[df['_is_dup']].drop(columns='_is_dup').reset_index(drop=True)
    
    return df_clean, df_dups


def deduplicate_file(input_file: Path, output_file: Path = None) -> dict:
    df = pd.read_excel(input_file)
    df = normalize_dataframe(df)
    before = len(df)
    
    df_clean, df_dups = find_duplicates(df)
    
    if output_file:
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        df_clean.to_excel(output_file, index=False)
    
    return {
        'before': before,
        'after': len(df_clean),
        'removed': len(df_dups),
        'clean': df_clean,
        'duplicates': df_dups,
    }


if __name__ == '__main__':
    # Тест: запускать как "python -m src.tools.deduplicator" из корня проекта
    base = Path(__file__).parent.parent.parent / 'examples'
    report = deduplicate_file(
        input_file=base / 'people.xlsx',
        output_file=base / 'people_clean.xlsx',
    )
    print(f'Было:    {report["before"]}')
    print(f'Удалено: {report["removed"]}')
    print(f'Осталось: {report["after"]}')