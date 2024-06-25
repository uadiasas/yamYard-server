# YumYard Backend

Это серверная часть приложения по обмену рецептами. Разработана с использованием Django и Django REST Framework.
Выполнил: Симонов Вадим, 1 группа, 3 курс, 5 команда.

## Свойства приложения

- Управление рецептами: добавление, просмотр, редактирование и удаление.
- Добавление рецептов в избранное.
- Подписки на авторов.
- Аутентификация с использованием Django's User модели.
- Рейтинг рецептов по пятибальной шкале.
- Поиск рецептов по названию, содержимому и категориям.

## Установка проекта

### Требования

- Python 3.11

### Шаги установки

1. **Клонирование репозитория:**

   ```bash
   git clone https://github.com/uadiasas/yamYard-server.git
   cd yamYard-server
   
2. **Создание и запуск контейнера:**

   ```bash
   docker compose build app
   docker compose up -d
   
3. **Выполнение миграций БД:**

   ```bash
   docker compose exec app bash
   python manage.py makemigrations
   python manage.py migrate
   
4. **Создание аккаунта администратора:**
Следуйте инструкциям по созданию суперпользователя, вводя имя пользователя, email (необязательно) и пароль.
   ```bash
   python manage.py createsuperuser
   
5. **Выход из командной строки контейнера:**

   ```bash
   exit

## Сервер, на котором уже развёрнут проект (сслыка на сваггер)
http://45.89.63.102:8000/api/docs/
