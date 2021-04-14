from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View

from .models import Product, Category, Cart, CartProduct, CarouselImages
from .forms import CartForm


def view(request):
    if 'cart_pk' not in request.session:
        cart = Cart.objects.create()
        cart_pk = cart.pk
        cart.save()
        request.session['cart_pk'] = cart_pk
    cart = Cart.objects.get(pk=request.session['cart_pk'])
    products = Product.objects.all()
    images = CarouselImages.objects.filter(category__name='На главной', is_active=True)
    context = {
        'products': products,
        'category': Category.objects.all(),
        'cart_product_count': cart.total_products,
        'images': images,
    }
    return render(request, 'base.html', context)


def product_view(request, slug):
    if 'cart_pk' not in request.session:
        cart = Cart.objects.create()
        cart_pk = cart.pk
        cart.save()
        request.session['cart_pk'] = cart_pk
    cart = Cart.objects.get(pk=request.session['cart_pk'])
    category = Category.objects.all()
    product = Product.objects.filter(slug=slug).first()
    context = {
        'cart_product_count': cart.total_products,
        'product': product,
        'category': category,
    }
    return render(request, 'product_detail.html', context)


def category_view(request, slug):
    if 'cart_pk' not in request.session:
        cart = Cart.objects.create()
        cart_pk = cart.pk
        cart.save()
        request.session['cart_pk'] = cart_pk
    cart = Cart.objects.get(pk=request.session['cart_pk'])
    category = Category.objects.all()
    product = Product.objects.filter(category__slug=slug)
    selected_category = Category.objects.filter(slug=slug).first()
    context = {
        'product': product,
        'category': category,
        'selected_category': selected_category,
        'cart_product_count': cart.total_products,
    }
    return render(request, 'category_detail.html', context)


def cart_view(request):
    if 'cart_pk' not in request.session:
        cart = Cart.objects.create()
        cart_pk = cart.pk
        cart.save()
        request.session['cart_pk'] = cart_pk
    cart = Cart.objects.get(pk=request.session['cart_pk'])
    category = Category.objects.all()
    products = CartProduct.objects.filter(cart=cart)
    cart.final_price_def()
    cart.total_products_def()
    context = {
        'category': category,
        'products': products,
        'cart_product_count': cart.total_products,
        'cart': cart,
    }
    return render(request, 'cart.html', context)


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart = Cart.objects.get(pk=request.session['cart_pk'])
        CartProduct.objects.get_or_create(cart=cart, product=product)
        return HttpResponseRedirect('/cart/')


def delete_from_cart(request, slug, cart_id):
    CartProduct.objects.get(cart__id=cart_id, product__slug=slug).delete()
    return HttpResponseRedirect('/cart/')


def change_qty(request, slug, cart_id):
    product = CartProduct.objects.get(cart__id=cart_id, product__slug=slug)
    product.qty = int(request.POST.get('qty'))
    product.save()
    return HttpResponseRedirect('/cart/')


def checkout(request):
    form = CartForm(request.POST or None)
    cart = Cart.objects.get(pk=request.session['cart_pk'])
    context = {
        'category': Category.objects.all(),
        'cart_product_count': cart.total_products,
        'form': form,
    }
    return render(request, 'checkout.html', context)


def checkout_post(request):
    form = CartForm(request.POST or None)
    if form.is_valid():
        cart = Cart.objects.get(pk=request.session['cart_pk'])
        cart.name = form.cleaned_data['name']
        cart.phone = form.cleaned_data['phone']
        cart.address = form.cleaned_data['address']
        cart.save()
        send_mail('Новый заказ', 'Ура, новый заказ с сайта', 'info@smartbit45.ru', ('crash-em@mail.ru', ))
    return HttpResponseRedirect('/')
