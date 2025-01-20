from django.db import models
from django.conf import settings
# Create your models here.
class Product(models.Model):
  title =models.CharField(max_length=100)
  body = models.TextField()
  date = models.DateTimeField(auto_now_add=True)
  image = models.ImageField(null=True)
  price = models.IntegerField(null=True)
  def __str__(self):
    return self.title

class Cart(models.Model):
    products = models.ManyToManyField(Product, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        """Tính tổng giá tiền của tất cả sản phẩm trong giỏ hàng."""
        return sum(item.total_price() for item in self.cartitem_set.all())

    def __str__(self):
        return f"Cart {self.id}"
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        """Tính tổng giá tiền của sản phẩm này trong giỏ hàng."""
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"
class Comment(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  body = models.TextField()
  date = models.DateTimeField(auto_now_add=True)
