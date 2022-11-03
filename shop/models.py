from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models

# таблица Продукты
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='product_name')
    code = models.CharField(max_length=255,
                            verbose_name='product_code')  # по этому полю различаем продукт (код продукта)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    unit = models.CharField(max_length=255, blank=True, null=True)  # единица измерения
    image_url = models.URLField(blank=True, null=True)  # ссылка на изображение продукта
    note = models.TextField(blank=True, null=True)  # комментарий к продукту

    class Meta:  # все элементы отображаются по дате создания
        ordering = ['pk']

    def __str__(self):
        return f'name: {self.name}, price: {self.price}'


# таблица Платежи
class Payment(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)  # поле связано с табл. User, имя модели User, on_delete - удаление платежей
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)  # сумма платежа
    time = models.DateTimeField(auto_now_add=True)  # время создания платежа, заполняется автоматически
    comment = models.TextField(blank=True, null=True)  # комментарий к платежу

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'name: {self.user} , price: {self.amount}'


# таблица Заказ + Корзина
class Order(models.Model):
    STATUS_CART = '1_cart'  # статус "Корзина"
    STATUS_WAITING_FOR_PAYMENT = '2_waiting_for_payment'  # статус "Ожидание платежа"
    STATUS_PAID = '3_paid'  # статус "Заказ оплачен"
    STATUS_CHOICES = [
        (STATUS_CART, 'cart'),
        (STATUS_WAITING_FOR_PAYMENT, 'waiting_for_payment'),
        (STATUS_PAID, 'paid')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # items = models.ManyToManyField(OrderItem, related_name='orders')  # возможность установить связь с OrderItem
    status = models.CharField(max_length=32, choices=STATUS_CHOICES,
                              default=STATUS_CART)  # статус покупки, выбор из трех элементов
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)  # сумма заказа
    creation_time = models.DateTimeField(auto_now_add=True)  # время создания заказа, заполняется автоматически
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, blank=True,
                                null=True)  # поле, связанное с платежами, которое совершит изменение статуса оплаты
    comment = models.TextField(blank=True, null=True)  # комментарий к заказу

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'name: {self.user}, amount: {self.amount}, status: {self.status}'

    @staticmethod
    def get_cart(user: User):
        cart = Order.objects.filter(user=user,
                                    status=Order.STATUS_CART
                                    ).first()
        if cart and (timezone.now() - cart.creation_time).days > 7:
            cart.delete()
            cart = None

        if not cart:
            cart = Order.objects.create(user=user,
                                        status=Order.STATUS_CART,
                                        amount=0
                                        )
        return cart

    def get_amount(self):
        amount = Decimal(0)
        for item in self.orderitem_set.all():
            amount += item.amount
        return amount

# каждый элемент заказа
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # связь с заказом
    product = models.ForeignKey(Product,
                                on_delete=models.PROTECT)  # связь с Продуктом, удалить продукт просто так нельзя
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # возможная скидка, по умолчанию 0

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'product: {self.product}, price: {self.price}'

    @property
    def amount(self):
        return self.quantity * (self.price - self.discount)

@receiver(post_save, sender=OrderItem) # сигнал, соответствующий сохранению объекта в базе данных
def recalculate_order_amount_after_save(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.save()

@receiver(post_delete, sender=OrderItem) # сигнал, соответствующий удалению объекта из базы данных
def recalculate_order_amount_after_delete(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.save()