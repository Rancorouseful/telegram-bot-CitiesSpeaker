# Бот для игры в города
#### Телеграм бот для игры в города, с возможностью выбора стран. Поддерживает сразу несколько игровых сессий.

## Как настроить

- Создать телеграмм бота

1. Cоздать нового бота через https://t.me/BotFather.

2. Получить токен.

3. Указать токен в файле ``config.py``:

```
# Токен от телеграм бота
token = ""
```

- Как добавить страны и города:

1. Создать **список из строк** городов. Список должен быть назван **кодом страны**:

```
RU = ["Москва", "Челябинск", "Владивосток"...]
```

2. Добавить строчку в список ``countries``. Строка должна быть составлена из **кода страны** и **эмодзи флага** этой страны:

```
countries = ['RU 🇷🇺']
```

3. Добавить **ключ** и **значение ключа** в словарь **all_domains**:

```
#'Код страны'(первая часть строки в countries): Код страны(название списка с городами)
all_domains = {'RU': RU}
```

