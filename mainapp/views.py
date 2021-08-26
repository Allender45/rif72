from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View

from .models import *
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
    promo = Promo.objects.all()
    subcategory = SubCategory.objects.filter(category__slug=slug)
    selected_category = Category.objects.filter(slug=slug).first()
    context = {
        'subcategory': subcategory,
        'category': category,
        'selected_category': selected_category,
        'cart_product_count': cart.total_products,
        'promo': promo,
    }
    return render(request, 'category.html', context)


def sub_category_view(request, slug):
    if 'cart_pk' not in request.session:
        cart = Cart.objects.create()
        cart_pk = cart.pk
        cart.save()
        request.session['cart_pk'] = cart_pk
    cart = Cart.objects.get(pk=request.session['cart_pk'])
    category = Category.objects.all()
    promo = Promo.objects.all()
    products = Product.objects.filter(category__slug=slug)
    selected_sub_category = SubCategory.objects.filter(slug=slug).first()
    context = {
        'selected_sub_category': selected_sub_category,
        'cart_product_count': cart.total_products,
        'promo': promo,
        'products': products,
        'category': category,
    }
    print(selected_sub_category.category)
    return render(request, 'sub_category.html', context)


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
        send_mail('Новый заказ', 'Ура, новый заказ с сайта', 'trash@smartbit45.ru', ('crash-em@mail.ru', ))
    return HttpResponseRedirect('/')


def home(request):
    if 'cart_pk' not in request.session:
        cart = Cart.objects.create()
        cart_pk = cart.pk
        cart.save()
        request.session['cart_pk'] = cart_pk
    cart = Cart.objects.get(pk=request.session['cart_pk'])
    products = Product.objects.all()
    promo = Promo.objects.all()
    images = CarouselImages.objects.filter(category__name='На главной', is_active=True)
    blog = Blog.objects.all()[:5]
    context = {
        'products': products,
        'category': Category.objects.all(),
        'cart_product_count': cart.total_products,
        'images': images,
        'promo': promo,
        'blog': blog,
    }
    return render(request, 'home.html', context)


def blog(request):
    if 'cart_pk' not in request.session:
        cart = Cart.objects.create()
        cart_pk = cart.pk
        cart.save()
        request.session['cart_pk'] = cart_pk
    cart = Cart.objects.get(pk=request.session['cart_pk'])
    promo = Promo.objects.all()
    blog = Blog.objects.all()
    context = {
        'category': Category.objects.all(),
        'cart_product_count': cart.total_products,
        'promo': promo,
        'blog': blog,
    }
    return render(request, 'blog.html', context)


def blog_detail(request, slug):
    if 'cart_pk' not in request.session:
        cart = Cart.objects.create()
        cart_pk = cart.pk
        cart.save()
        request.session['cart_pk'] = cart_pk
    cart = Cart.objects.get(pk=request.session['cart_pk'])
    promo = Promo.objects.all()
    blog = Blog.objects.filter(slug=slug).first()
    context = {
        'category': Category.objects.all(),
        'cart_product_count': cart.total_products,
        'promo': promo,
        'blog': blog,
    }
    return render(request, 'blog_detail.html', context)
