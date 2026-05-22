from django.contrib import admin
from .models import Category, FoodItem, Cart, CartItem, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'is_available', 'is_veg']
    list_filter = ['category', 'is_available', 'is_veg']
    list_editable = ['price', 'is_available']
    search_fields = ['name']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['food_item', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'payment_method', 'payment_done', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_done']
    list_editable = ['status']
    search_fields = ['user__username', 'phone']
    inlines = [OrderItemInline]
    readonly_fields = ['user', 'total_amount', 'address', 'phone', 'created_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']