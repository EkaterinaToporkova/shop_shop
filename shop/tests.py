import zoneinfo
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from shop.models import Product, Payment, OrderItem, Order


class TestDataBase(TestCase):
    fixtures = [
        'shop/fixtures/mydata.json'
    ]

    # извлекаем супер пользователя
    def setUp(self):
        self.user = User.objects.get(username='root')
        self.p = Product.objects.all().first()

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

        # Нет корзины
        self.assertEqual(self.find_cart_number(), 0)
        # 2. Корзина только что создана
        Order.get_cart(self.user)
        self.assertEqual(self.find_cart_number(), 1)
        # 3. Проверить, что получена так корзина, которая создана, а не создалась новая
        Order.get_cart(self.user)
        self.assertEqual(self.find_cart_number(), 1)

    def test_cart_older_7_day(self):
        '''Если корзина старше 7 дней, она должна быть удалена
        1. Получаем корзину и искусственно состариваем ее
        '''
        cart = Order.get_cart(self.user)
        cart.creation_time = timezone.datetime(2000, 1, 1, tzinfo=zoneinfo.ZoneInfo('UTC'))
        cart.save()
        cart = Order.get_cart(self.user)
        self.assertEqual((timezone.now() - cart.creation_time).days, 0)

    def test_recalculate_order_amount_after_changing_ordertime(self):
        '''Перерасчет суммы заказа после каждого изменения
        1. Получаем сумму до какого-либо изменения
        2. -------''-------- после добавления элемента
        3. -------''-------- после удаления элемента
        '''

        # 1. Получаем сумму до какого-либо изменения
        cart = Order.get_cart(self.user)
        self.assertEqual(cart.amount, Decimal(0))

        # 2. -------''-------- после добавления элемента
        i = OrderItem.objects.create(order=cart, product=self.p, price=2, quantity=2)
        i = OrderItem.objects.create(order=cart, product=self.p, price=2, quantity=3)
        cart = Order.get_cart(self.user)
        self.assertEqual(cart.amount, Decimal(10))

        # 3. -------''-------- после удаления элемента
        i.delete()
        cart = Order.get_cart(self.user)
        self.assertEqual(cart.amount, Decimal(4))