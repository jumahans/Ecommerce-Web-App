from django.contrib import admin
from . import models

# from .models import UserImage
# Register your models here.
class gallerlyinline(admin.TabularInline):
    model = models.Gallery
    extra = 1

class varianinline(admin.TabularInline):
    model = models.Variant
    extra = 1

class VariantItem(admin.TabularInline):
    model = models.VariantItem
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image']
    prepopulated_fields = {'slug': ('title',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'quantity', 'image', 'description', 'date', 'status']
    list_editable = ['price', 'quantity', 'image']
    inlines = [gallerlyinline, varianinline]

class MyCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price', 'quantity', 'cart_id']
    list_editable = ['quantity']
    search_fields = ['cart_id', 'product__name', 'user__username']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order_id', 'payment_status', 'payment_method', 'order_status']
    list_editable = ['payment_status', 'order_status']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'total_products']
    list_editable = ['quantity', 'price']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'ratting', 'reply']
    list_editable = ['ratting']
    search_fields = ['user__username', 'product__name', 'ratting']

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'vendor']
    search_fields = ['code', 'vendor__username']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']
    search_fields = ['user__username']

# @admin.register(UserImage)
# class UserImageAdmin(admin.ModelAdmin):
#     list_display = ['user', 'image']
#     ordering = ['user']
#     list_filter = ['user']

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.MyCart, MyCartAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.Coupon, CouponAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
