from django.contrib import admin
from .models import Product,Cart,CartItem,Comment
# Register your models here.
class CommentInline(admin.TabularInline):
  model=Comment
class PostAdmin(admin.ModelAdmin):
  list_display=['title','date']
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