from django.contrib import admin
from .models import Product,Cart,CartItem
# Register your models here.

class PostAdmin(admin.ModelAdmin):
  list_display=['title','date']
  list_filter=['date']
  search_fields=['id']
admin.site.register(Product, PostAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)