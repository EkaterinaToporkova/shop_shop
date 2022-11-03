from django.contrib.auth.models import User
from django.test import TestCase
from shop.models import Product, Payment, OrderItem, Order


class TestDataBase(TestCase):
    fixtures = [
        'shop/fixtures/mydata.json'
    ]

    # извлекаем супер пользователя
    def setUp(self):
        self.user = User.objects.get(username='root')

    # проверяем, существует ли пользователь
    def test_user_exists(self):
        users = User.objects.all()
        user = users.first()
        self.assertEqual(user.username, 'root')
        self.assertTrue(user.is_superuser)

    # проверяем пароль суперпользователя
    def test_user_password(self):
        self.assertTrue(self.user.check_password('123'))

    # проверяем, что во всех таблицах находится больше 1 значения
    def test_all_date(self):
        self.assertGreater(Product.objects.all().count(), 0)
        self.assertGreater(Order.objects.all().count(), 0)
        self.assertGreater(OrderItem.objects.all().count(), 0)
        self.assertGreater(Payment.objects.all().count(), 0)

    # подчитываем корзины конкретного пользователя
    def find_cart_number(self):
        cart_number = Order.objects.filter(user=self.user,
                                           status=Order.STATUS_CART
                                           ).count()
        return cart_number

    # проверяем количество корзин пользователя
    def test_functional_get_cart(self):
        '''
        1. Нет корзины
        2. Корзина только что создана
        3. Проверить, что получена так корзина, которая создана, а не создалась новая
        =============================================================================
        Добавим @staticmethod Order.get_cart(user)
        '''