#Тестовое задание: Реализация Django + Stripe API.
Приложение позволяет заказывать товары со скидками и налогами и покупать их через платежную систему Stripe.

## 1. Функционал

*  Реализованы страницы просмотра товара и заказа с интеграцией платежной системы.
*  Использование сессий Stripe для безопасной обработки платежей.
*  Возможность добавления налогов и скидок к любому заказу через админ-панель.
*  Поддержка платежей в USD и EUR.
*  Контейнеризация приложения(Docker). 

## 2. Технологии
* Python3.13
* Django
* Stripe API
* Sqlite3
* Docker

## 3. Запуск проекта
* через Docker

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/vikagit11/stripe_test
   cd stripe_test
   ```
2. Создать файл с переменными окружения: файл .env в корне проекта и добавить туда  ключи:
```text
STRIPE_PUBLIC_KEY=
STRIPE_SECRET_KEY=
DJANGO_SECRET_KEY=
DEBUG=True

3. Запустить проект:
   ```bash 
    docker-compose up --build
    ```
4. Создать суперпользователя:
   ```bash
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    ```
5. Открыть админку: http://127.0.0.1:8000/admin/

* локально

1. Создать и активировать виртуальное окружение:
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Mac/Linux: source venv/bin/activate
   ```

2. Установить зависимости: 
   ```bash 
   pip install -r requirements.txt
   ```
3. Настроить .env
4. Применить миграции и запустить сервер:
   ```bash                         
   python manage.py migrate
   python manage.py runserver 
   ```
      Сервер запустится: http://127.0.0.1:8000/
5. Создать суперпользователя: 
   ```bash 
   python manage.py createsuperuser
   ```
## 4.Тестирование оплаты
Проект работает в тестовом режиме Stripe. Для проверки успешной оплаты использовать следующие данные:

- Номер карты: `4242 4242 4242 4242`
- Срок действия:Любая будущая дата (например, `12/30`)
- CVC: Любые 3 цифры (например, `123`)
Полный список тестовых карт доступен в официальной документации Stripe https://stripe.com/docs/testing.








