"""
Pipeline — конвейер очистки CRM-таблицы.

Прогоняет файл через все этапы:
    1. Загрузка
    2. Нормализация (телефоны, email, ФИО, города)
    3. Удаление дубликатов
    4. Сохранение результатов + отчёт

Использование:
    python src/pipeline.py --input examples/people.xlsx
    python src/pipeline.py --input dirty.xlsx --output clean.xlsx
"""
import argparse
from pathlib import Path

import pandas as pd

from .tools.normalizer import normalize_dataframe
from .tools.deduplicator import find_duplicates  # см. ниже — нужна новая функция


def run_pipeline(input_file: Path, output_dir: Path) -> dict:
    """
    Основной конвейер. Возвращает словарь с отчётом.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    report = {'input': str(input_file)}

    # ---------- 1. Загрузка ----------
    print(f'\n📂 Загрузка: {input_file}')
    df = pd.read_excel(input_file)
    report['loaded'] = len(df)
    print(f'   Строк загружено: {len(df)}')

    # ---------- 2. Нормализация ----------
    print('\n🔧 Нормализация данных...')
    df = normalize_dataframe(df)
    print('   Телефоны, email, ФИО, города приведены к единому виду')

    # ---------- 3. Дедупликация ----------
    print('\n🧹 Поиск дубликатов...')
    before = len(df)
    df['_is_dup'] = df.duplicated(subset=['Телефон', 'Email'], keep='first')

    df_clean = df[~df['_is_dup']].drop(columns='_is_dup').reset_index(drop=True)
    df_dups = df[df['_is_dup']].drop(columns='_is_dup').reset_index(drop=True)

    report['before_dedup'] = before
    report['after_dedup'] = len(df_clean)
    report['duplicates'] = len(df_dups)
    print(f'   Удалено дубликатов: {len(df_dups)}')
    print(f'   Осталось строк:     {len(df_clean)}')

    # ---------- 4. Сохранение ----------
    clean_path = output_dir / 'output_clean.xlsx'
    dup_path = output_dir / 'output_duplicates.xlsx'

    df_clean.to_excel(clean_path, index=False)
    df_dups.to_excel(dup_path, index=False)

    report['clean_file'] = str(clean_path)
    report['duplicates_file'] = str(dup_path)

    print(f'\n💾 Сохранено:')
    print(f'   Чистый файл:       {clean_path}')
    print(f'   Удалённые строки:  {dup_path}')

    return report


def print_report(report: dict) -> None:
    """Печатает итоговый отчёт в консоль."""
    print('\n' + '=' * 45)
    print('   ОТЧЁТ ОБ ОЧИСТКЕ')
    print('=' * 45)
    print(f'  Исходный файл:       {report["input"]}')
    print(f'  Загружено строк:     {report["loaded"]}')
    print(f'  Дубликатов удалено:  {report["duplicates"]}')
    print(f'  Осталось строк:      {report["after_dedup"]}')
    print('=' * 45)


def main():
    parser = argparse.ArgumentParser(
        description='Очистка CRM-таблицы: нормализация + удаление дубликатов.'
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Путь к исходному Excel-файлу',
    )
    parser.add_argument(
        '--output', '-o',
        default=None,
        help='Папка для сохранения результатов (по умолчанию — папка examples)',
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f'❌ Файл не найден: {input_path}')
        return

    output_dir = Path(args.output) if args.output else Path(__file__).parent.parent / 'examples'

    report = run_pipeline(input_path, output_dir)
    print_report(report)


if __name__ == '__main__':
    main()