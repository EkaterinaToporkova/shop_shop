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
- tests.py
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


### Требования к БД
_____

Наша корзина - это заказ со статусом cart. Просто после нажатия кнопки “Перейти к оплате” этот статус меняется на waiting_for_payment

Структура данных будет состоять из 4-х таблиц:

- Таблица Заказа Order
- Таблица Элементов заказа OrderItems (или элементов, из которых состоит каждый заказ)
- Таблица Товаров Product (ассортимента)
- Таблица Оплат Payment
- Таблица Рецептов супов Recipe
P. S. список таблиц будет расти.

Требования к бизнес-логике БД

- При выборе товара пользователем, товар должен в выбранном количестве добавляться в корзину Cart, которая должна создаваться автоматически (если, конечно, она уже не была создана к этому моменту).
- Корзина, не перешедшая в статус Заказа в течении 7 дней, должна автоматически удаляться при первом же вызове метода get_cart(user).
- При каждом новом добавлении (удалении, изменении) количества (или цены) товара, общая сумма заказа должна автоматически пересчитываться.
- После завершения набора/изменения Корзины и перехода к оплате, Корзина должна менять статус (если она не пустая!) и становиться Заказом, ожидающим оплаты (waiting_for_payment).
- Необходим метод get_unpaid_orders(user), который позволит получить общую сумму неоплаченных заказов (status=waiting_for_payment) по указанному пользователю.
- Необходим метод get_balance(user), который позволит получить баланс по счёту указанного пользователя.
- Смена статуса на waiting_for_payment автоматически запускает проверку баланса текущего пользователя. Если сумма баланса >= сумме заказа, то Заказ изменяет свой статус на оплаченный. При этом параллельно создаётся оплата, равная (минус) сумме заказа (что сразу же после оплаты уменьшает баланс счёта клиента на сумму заказа).
- Внесение оплаты автоматически запускает механизм проверки всех неоплаченных заказов, начиная с самого старого. Если внесённой суммы оплаты достаточно для оплаты нескольких заказов, ожидающих оплаты, то все эти заказы изменяют свой статус на оплаченный. При этом параллельно формируются оплаты, равные (минус)сумме каждого заказа (что сразу же после оплаты уменьшает баланс счёта клиента на сумму заказов).

Для написания тестов используется готовый модуль tests.py - переносим требования к БД в код тестов/


Так как сайт еще не был развернут на серевере прикладываю скрины.

### Рецепты
![Рецепты](https://github.com/EkaterinaToporkova/shop_shop/blob/main/photo_2022-12-08_10-35-53.jpg)

### Одна из категорий
![Одна из категорий](https://github.com/EkaterinaToporkova/shop_shop/blob/main/photo_2022-12-08_10-36-51.jpg)

### детализация рецепта
![детализация рецепта](https://github.com/EkaterinaToporkova/shop_shop/blob/main/photo_2022-12-08_10-37-01.jpg)

### видео-рецепта
![видео-рецепта](https://github.com/EkaterinaToporkova/shop_shop/blob/main/%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE.jpg)

### детализация продукта (можно перейти из страницы с рецептами и с шапки)
![детализация продукта](https://github.com/EkaterinaToporkova/shop_shop/blob/main/photo_2022-12-08_10-38-36.jpg)

### список продуктов
![список продуктов](https://github.com/EkaterinaToporkova/shop_shop/blob/main/photo_2022-12-08_10-39-21.jpg)

### вход
![вход](https://github.com/EkaterinaToporkova/shop_shop/blob/main/photo_2022-12-08_10-41-15.jpg)

### регистрация
![вход](https://github.com/EkaterinaToporkova/shop_shop/blob/main/photo_2022-12-08_10-41-48.jpg)

### корзина
![вход](https://github.com/EkaterinaToporkova/shop_shop/blob/main/cart.jpg)
