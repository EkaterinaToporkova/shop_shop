from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone


# таблица Продукты
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='product_name')
    code = models.CharField(max_length=255,
                            verbose_name='product_code')  # по этому полю различаем продукт (код продукта)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    unit = models.CharField(max_length=255, blank=True, null=True)  # единица измерения
    image_url = models.ImageField(upload_to='img_product')  # путь на изображение продукта
    note = models.TextField(blank=True, null=True)  # комментарий к продукту

    class Meta:  # все элементы отображаются по дате создания
        ordering = ['pk']

    def __str__(self):
        return f'name: {self.name}, price: {self.price},  image_url: {self.image_url}, pk: {self.code}'


class Product_image(models.Model):
    image = models.ImageField(upload_to='img_product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')

    def __str__(self):
        return f'{self.product.name} image'


# @property
# def sorted_image_set(self):
#     return self.product_images.order_by('time_created')


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

    @staticmethod
    def get_balance(user: User):
        amount = Payment.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum']
        return amount or Decimal(0)


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
        return f'name: {self.user}, amount: {self.amount}, status: {self.status}'  # отображение в БД

    @staticmethod
    def get_cart(user: User):  # корзина до каких-либо изменений
        cart = Order.objects.filter(user=user,
                                    status=Order.STATUS_CART
                                    ).first()
        if cart and (timezone.now() - cart.creation_time).days > 7:
            cart.delete()  # корзина удаляется, если ей больше 7 дней
            cart = None

        if not cart:  # если корзины не существует, то она создается
            cart = Order.objects.create(user=user,
                                        status=Order.STATUS_CART,
                                        amount=0
                                        )
        return cart

    def get_amount(
            self):  # общая сумма неоплаченных заказов, которая вычисляется из маленьких сумм каждого элемента в OrderItem
        amount = Decimal(0)
        for item in self.orderitem_set.all():  # находим сумму каждого элемента Order_item, который принадлежит заказу
            amount += item.amount  # увеличиваем сумму на значение amount, которое нашли в def amount() в OrderItem каждого элемента
        return amount

    def make_order(self):
        item = self.orderitem_set.all()
        if item and self.status == Order.STATUS_CART:
            self.status = Order.STATUS_WAITING_FOR_PAYMENT
            self.save()
            auto_payment_unpaid_orders(self.user)

    @staticmethod
    def get_amount_of_unpaid_orders(user: User):
        amount = Order.objects.filter(user=user,
                                      status=Order.STATUS_WAITING_FOR_PAYMENT
                                      ).aggregate(Sum('amount'))['amount__sum']
        return amount or Decimal(0)


# в этом классе все элементЫ, которые лежат в Корзине + перерасчет суммы всего заказа
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # связь с заказом
    product = models.ForeignKey(Product,
                                on_delete=models.PROTECT)  # связь с Продуктом, удалить продукт просто так нельзя
    quantity = models.PositiveIntegerField(default=1)  # количество, вводим вручную
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # возможная скидка, по умолчанию 0

    class Meta:
        ordering = ['pk']
        # constraints = [
        #     models.UniqueConstraint(fields=['order', 'product'], name='unique')
        # ]

    def __str__(self):
        return f'product: {self.product}, amount: {self.amount}'  # отображение в БД

    @property
    def amount(self):  # перерасчет amount элемента с учетом количества и скидки
        return self.quantity * (self.price - self.discount)


@transaction.atomic()
def auto_payment_unpaid_orders(user: User):  # автоплатеж неоплаченных заказов
    unpaid_orders = Order.objects.filter(user=user,
                                         status=Order.STATUS_WAITING_FOR_PAYMENT)
    for order in unpaid_orders:
        if Payment.get_balance(user) < order.amount:
            break
        order.payment = Payment.objects.all().last()
        order.status = Order.STATUS_PAID
        order.save()
        Payment.objects.create(user=user,
                               amount=-order.amount)


@receiver(post_save, sender=OrderItem)  # после сохранения OrderItem, идет функция recalculate_order_amount_after_save()
def recalculate_order_amount_after_save(sender, instance, **kwargs):  # instance - подает сигнал о сохранении
    order = instance.order  # получим заказ, к которому был послан сигнал о сохранении
    order.amount = order.get_amount()  # получаем сумму для этого заказа
    order.save()  # сохраняем, чтобы отразить изменение в базе данных


@receiver(post_delete, sender=OrderItem)  # сигнал, соответствующий удалению объекта из базы данных
def recalculate_order_amount_after_delete(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.save()


@receiver(post_save, sender=Payment)  # сигнал, соответствующий сохранению объекта в базе данных
def auto_payment(sender, instance, **kwargs):
    user = instance.user
    auto_payment_unpaid_orders(user)


class Recipe(models.Model):
    code = models.CharField(max_length=255,
                            verbose_name='recipe_code', default=0)
    name = models.CharField(max_length=255, verbose_name='recipe_name')
    description = models.CharField(max_length=1000, verbose_name='description')
    product_list = models.ManyToManyField(Product)
    image_recipe = models.ImageField(upload_to='image_recipe')
    video_url = models.URLField(blank=True, null=True)
    recipe_note = models.TextField(blank=True, null=True)
    image_thousand_on_thousand = models.ImageField(upload_to='image_thousand_on_thousand', null=True)

    class Meta:  # все элементы отображаются по дате создания
        ordering = ['pk']

    def __str__(self):
        return f'{self.name}'
