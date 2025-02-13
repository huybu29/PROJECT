from django.contrib import admin
from .models import Product,Cart,CartItem,Comment,Category,Order,OrderItem
# Register your models here.
class CommentInline(admin.TabularInline):
  model=Comment
class PostAdmin(admin.ModelAdmin):
  list_display=['body','date']
  list_filter=['date']
  search_fields=['id']
  inlines=[CommentInline]
admin.site.register(Product, PostAdmin)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra=1

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name']
admin.site.register(Category)   

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra=1
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)