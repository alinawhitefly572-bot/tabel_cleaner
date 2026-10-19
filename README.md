## Возможности
- Нормализация телефонов, email, ФИО, городов
- Очистка от пустых и бесполезных строк
- Удаление лишних пробелов
- Удаление дубликатов
- Отчёт: сколько было, что удалено, сколько осталось
## Пример работы



![Отчёт в консоли](docs/screenshot_console.png)

Результат: 100 строк → 93 после очистки.

![до и после](docs/screenshot_before_after.png)

##Автор

tg:@LiaAsami 

```bash
python -m src.pipeline -i examples/people.xlsx

![до и после](docs/screenshot_before_after.png)
