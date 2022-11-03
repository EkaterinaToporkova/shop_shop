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
        users_number = users.coint()
        user = users.first()
        self.assertEqual(users_number, 1)
        self.assertEqual(user.name, 'root')
        self.assertTrue(user.is_superuser)

    # проверяем пароль
    def test_user_password(self):
        self.assertTrue(self.user.check_password('123'))
