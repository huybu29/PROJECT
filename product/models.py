from django.db import models
from django.conf import settings
# Create your models here.
class Product(models.Model):
  category =models.CharField(max_length=100)
  body = models.TextField()
  date = models.DateTimeField(auto_now_add=True)
  image = models.ImageField(null=True)
  price = models.IntegerField(null=True)
  def __str__(self):
    return self.body       
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart",null=True)
    

    def total_price(self):
        """Tính tổng giá tiền của tất cả sản phẩm trong giỏ hàng."""
        return sum(item.total_price() for item in self.items.all())
    def tax(self):
       return self.total_price()//20
    def total(self):
       return self.total_price()+self.tax()
    def __str__(self):
        return f"Cart of {self.user}"
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.  CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def total_price(self):
        return self.product.price * self.quantity
    def __str__(self):
        return f"{self.quantity} x {self.product.body} in Cart {self.cart.id}"
class Comment(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  body = models.TextField()
  date = models.DateTimeField(auto_now_add=True)
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(null=True)
    address=models.TextField(null=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.body} in Order {self.order.id}"