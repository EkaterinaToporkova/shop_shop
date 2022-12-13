from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic import ListView, DetailView, DeleteView

from shop.forms import AddQuantityForm
from shop.models import Product, Order, Product_image, OrderItem


class ProductsListView(ListView):
    model = Product
    template_name = 'shop/shop.html'


class ProductsDetailView(DetailView):
    model = Product
    template_name = 'shop/shop-details.html'


@login_required(login_url=reverse_lazy(
    'register'))  # работу функции add_item_to_cart() может вызвать только залогиненный пользователь
def add_item_to_cart(request, pk):
    if request.method == 'POST':
        quantity_form = AddQuantityForm(request.POST)
        if quantity_form.is_valid():  # если форма прошла валидацию, то создаётся объект quantity
            quantity = quantity_form.cleaned_data['quantity']
            if quantity:
                cart = Order.get_cart(
                    request.user)  # метод get_cart способен обеспечить нужной корзиной - объектом cart
                product = get_object_or_404(Product, pk=pk)
                if OrderItem.objects.filter(product=product).exists():
                    order_items = cart.orderitem_set.filter(product=product)
                    for it in order_items:
                        it.quantity += quantity
                        it.save()
                        cart.save()
                else:
                    cart.orderitem_set.create(product=product,
                                              quantity=quantity,
                                              price=product.price)  # с помощью cart.orderitem_set.create() создаём новый объект модели OrderItem

                cart.save()  # фиксируем связь этого объекта с корзиной заказа
                # return redirect('cart_view')
        else:
            pass
    return redirect(request.META['HTTP_REFERER'])


# Из объекта cart в шаблоне будут извлекаться только данные, относящиеся к самой корзине (в нашем случае - только сумма заказа). Данные по каждой позиции заказа item мы получим результате цикла по объекту items:
@login_required(login_url=reverse_lazy('signin'))
def cart_view(request):
    cart = Order.get_cart(request.user)
    items = cart.orderitem_set.all()
    context = {
        'cart': cart,
        'items': items
    }
    return render(request, 'shop/cart.html', context)


def home_page(request):
    products = Product.objects.all()
    images = Product_image.objects.all()
    context = {'products': products, 'images': images}
    return render(request, 'product/home.html', context)  # TODO разобраться, почему тут home.html


@method_decorator(login_required,
                  name='dispatch')  # работу класса CartDeleteIem может вызвать только залогиненный пользователь
class CartDeleteItem(DeleteView):
    model = OrderItem
    template_name = 'shop/cart.html'
    success_url = reverse_lazy('cart_view')

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(order__user=self.request.user)
        return qs


@login_required(login_url=reverse_lazy('signin'))
def make_order(request):
    cart = Order.get_cart(request.user)
    # cart.make_order()
    return redirect('checkout')

#TODO: тут будет функция, которая переводит платеж в статус "Ожидание платежа"


@login_required(login_url=reverse_lazy('signin'))
def checkout_view(request):
    cart = Order.get_cart(request.user)
    items = cart.orderitem_set.all()
    context = {
        'cart': cart,
        'items': items
    }
    return render(request, 'shop/checkout.html', context)
