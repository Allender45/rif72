from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import *


class BlogAdminForm(forms.ModelForm):
    text = forms.CharField(label='Текст', widget=CKEditorUploadingWidget())
    class Meta:
        model = Blog
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'category', 'price', 'get_photo')

    def get_photo(self, object):
        return mark_safe(f'<img src="{object.image.url}" width="50">')
    get_photo.short_description = 'Изображение'


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address')


class CartProductAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'qty', 'total_price')


class CartProductInline(admin.TabularInline):
    model = CartProduct
    extra = 0


class CartAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_products', 'final_price', 'finished', 'phone', 'address', 'created',)
    inlines = [CartProductInline, ]
    list_filter = ('created', 'finished', )
    search_fields = ('phone', 'name', )
    list_editable = ('finished', )


class CarouselCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


class CarouselImagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'get_photo', 'is_active', )
    list_filter = ('category', )
    list_editable = ('is_active', )

    def get_photo(self, object):
        return mark_safe(f'<img src="{object.image.url}" width="100">')
    get_photo.short_description = 'Изображение'


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_photo', 'date', 'published', )
    list_editable = ('published', )
    prepopulated_fields = {"slug": ("title",)}
    form = BlogAdminForm

    def get_photo(self, object):
        return mark_safe(f'<img src="{object.image_small.url}" width="100">')
    get_photo.short_description = 'Изображение'


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_photo', 'date', 'published', )
    list_editable = ('published', )
    prepopulated_fields = {"slug": ("name",)}

    def get_photo(self, object):
        return mark_safe(f'<img src="{object.small_image.url}" width="100">')
    get_photo.short_description = 'Изображение'


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_photo', )
    prepopulated_fields = {"slug": ("name",)}

    def get_photo(self, object):
        return mark_safe(f'<img src="{object.image.url}" width="100">')
    get_photo.short_description = 'Изображение'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CarouselCategory, CarouselCategoryAdmin)
admin.site.register(CarouselImages, CarouselImagesAdmin)
