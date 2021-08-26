from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField('Изображение', upload_to='categories', null=True, blank=True)
    description = models.CharField('Описание', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.slug)])


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    category = models.ForeignKey('SubCategory', on_delete=models.PROTECT, verbose_name='Категория продукта')
    description = models.TextField(max_length=2000, verbose_name='Описание продукта')
    image = models.ImageField(verbose_name='Изображение')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена продукта')
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.slug)])


class CartProduct(models.Model):
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.PROTECT, related_name='related_products')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар в корзине', null=True)
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество')
    total_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Общая стоимость', default=0)

    def __str__(self):
        return f'Продукт: {self.product.name} (для корзины)'

    class Meta:
        verbose_name = 'Товар для корзины'
        verbose_name_plural = 'Товары для корзины'

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.qty
        return super(CartProduct, self).save()


class Cart(models.Model):
    total_products = models.PositiveIntegerField(default=0, verbose_name='Товаров')
    final_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Общая цена', default=0)
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True)
    address = models.CharField(max_length=500, verbose_name='Адрес', blank=True)
    name = models.CharField(max_length=250, verbose_name='Имя', default='User', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)
    finished = models.BooleanField(default=False, verbose_name='Завершён', blank=True)
    comment = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Комментарии')
    products = models.ForeignKey(CartProduct, blank=True, verbose_name='Товары в корзине',
                                      related_name='related_cart', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def final_price_def(self):
        self.final_price = 0
        for item in CartProduct.objects.filter(cart=self.id):
            self.final_price += item.total_price
        self.save()

    def total_products_def(self):
        self.total_products = 0
        for item in CartProduct.objects.filter(cart=self.id):
            self.total_products += item.qty
        self.save()

class Customer(models.Model):
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=500, verbose_name='Адрес')
    name = models.CharField(max_length=250, verbose_name='Имя', default='User')

    def __str__(self):
        return f'Покупатель: {self.name}'

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class CarouselCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Слайдеры'
        verbose_name_plural = 'Слайдеры'


class CarouselImages(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    category = models.ForeignKey(CarouselCategory, verbose_name='Категория', on_delete=models.PROTECT)
    image = models.ImageField(verbose_name='Изображение')
    is_active = models.BooleanField(default=True, verbose_name='Активное')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Изображение для слайдера'
        verbose_name_plural = 'Изображения для слайдера'


class Blog(models.Model):
    title = models.CharField('Заголовок', max_length=250)
    text = models.TextField('Текст', max_length=2000)
    short_text = models.TextField('Описание', max_length=500, blank=True, null=True)
    image_large = models.ImageField('Большое изображение', upload_to='img/blog/large')
    image_small = models.ImageField('Маленькое изображение', upload_to='img/blog/small')
    slug = models.SlugField(unique=True)
    date = models.DateField('Дата', default=timezone.now)
    published = models.BooleanField('Опубликовано', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блог'

    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.slug)])


class Promo(models.Model):
    name = models.CharField('Название', max_length=250)
    text = models.TextField('Текст', max_length=2000)
    short_text = models.TextField('Короткий текст', max_length=1000)
    image = models.ImageField('Изображение', upload_to='promo')
    small_image = models.ImageField('Превью', upload_to='promo')
    slug = models.SlugField(unique=True)
    date = models.DateField('Дата', default=timezone.now)
    published = models.BooleanField('Опубликовано', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'


class SubCategory(models.Model):
    name = models.CharField('Название', max_length=250)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField('Изображение', upload_to='categories', null=True, blank=True)
    description = models.TextField('Описание', max_length=1000, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def get_absolute_url(self):
        return reverse('sub_category_detail', args=[str(self.slug)])
