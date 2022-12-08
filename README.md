## Shop-shop
______

<b>Shop-shop</b> - это интернет-магазин по продаже продуктов, совмещенный с рецептами.
____
Часто бывает такое, что, когда собираешься приготовить обед, ужин или что-либо еще, обнаруживаешь, что дома не хватает продуктов для того, чтобы осуществить желаемое. Сайт поможет найти не только рецепт блюда, которое понравилось, но и купить необходимые ингредиенты здесь же, с доставкой на дом.

Сайт разработан с помощью видео-уроков [Django Drop Shipping Store](https://www.youtube.com/playlist?list=PLz8SX0iNPyAIlXZYQT0oafz_ZxNCYjDGd)
_____

Для написания проекта были использованы:

- Django 4.1
- CSS
- SQLite3
- HTML-шаблон с сайта: https://colorlib.com/
____

На сайте присутствуют основные страницы: 

- Рецепты - основная страница, на которой расположены категории рецептов.
- Магазин:
    - Магазин - список продуктов
    - Корзина
    - Оплата
- О нас
- Контакты
- Вход/Регистрация/Выход (в случае, если пользователь вошел, появляется изображение человека)

![file](https://github.com/EkaterinaToporkova/shop_shop/blob/main/header.jpg)
_____________

### Функционал сайта
____
Таблица товаров - плоская, т.е. без категорий/подкатегорий.
Выбранный товар с установленным количеством автоматически попадает в корзину. Если корзины для этого пользователя ещё нет, она создаётся, если уже есть - дополняется.
Если товары из корзины отправлены на оплату, то корзина обнуляется и появляется Заказа, со статусом “ожидающий оплаты”.
Для учёта оплат должна быть создана таблица платежей. Если сумма зачисленной оплаты больше или равна сумме заказа, то Заказ меняет статус на “оплаченный”, а в самой таблице платежей формируется “отрицательный” платёж с “минус-суммой”. Таким образом, для определения баланса счёта клиента не надо будет создавать новой таблицы баланса. Кроме того эта схема позволит также решить вопрос с онлайн оплатой: при подключении агрегатора онлайн оплаты, системе нужно будет всего лишь создать платёж, равный сумме полученной оплаты. Этого будет достаточно для автоматического перевода Заказа в категорию оплаченного.

И предусматриваем работу с платежами по банку:
- После каждой оплаты автоматически проверяем неоплаченные заказы. Если их несколько, то оплачиваем начиная с самого “старого”.
- При создании Заказа, ожидающего оплату, также проверяем, есть ли остаток по счёту клиента. И если сумма остатка больше или равна сумме заказа - автоматически переводим Заказ в разряд оплаченных и вычитаем из остатка сумму заказа.











