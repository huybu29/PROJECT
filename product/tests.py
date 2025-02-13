from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category, Cart, CartItem
from django.core.files.uploadedfile import SimpleUploadedFile
class ViewsTestCase(TestCase):
    def setUp(self):
        # Khởi tạo client (giả lập trình duyệt)
        self.client = Client()

        # Tạo user test
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Tạo danh mục sản phẩm
        self.category = Category.objects.create(name="Test Category")
        image = SimpleUploadedFile(
        name="test_image.jpg",
        content="",
        content_type="image/jpeg"
    )
        # Tạo sản phẩm
        self.product = Product.objects.create(
            category="Test Category",
            body="This is a test product",
            price=100,
            image=image
        )

        # Tạo giỏ hàng cho user
        self.cart = Cart.objects.create(user=self.user)

    # 1️⃣ Kiểm tra trang danh sách sản phẩm
    def test_list_view(self):
        response = self.client.get(reverse('bl'))  # Trang danh sách sản phẩm
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bl/bl.html")
        self.assertContains(response, self.product.body)  # Kiểm tra sản phẩm xuất hiện

    # 2️⃣ Kiểm tra xem chi tiết sản phẩm
    def test_post_view(self):
        response=self.client.get(reverse('product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bl/post.html")
        self.assertContains(response, self.product.body)

    # 3️⃣ Kiểm tra thêm sản phẩm vào giỏ hàng
    def test_add_to_cart_view(self):
        self.client.login(username="testuser", password="testpassword")  # Đăng nhập
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]), {"quantity": 2})

        self.assertEqual(response.status_code, 302)  # Redirect về trang chủ "/"
        cart_item = CartItem.objects.filter(cart=self.cart, product=self.product).first()
        self.assertIsNotNone(cart_item)  # Kiểm tra sản phẩm có trong giỏ
        self.assertEqual(cart_item.quantity, 2)  # Đúng số lượng

    # 4️⃣ Kiểm tra xem giỏ hàng
    def test_cart_view(self):
        self.client.login(username="testuser", password="testpassword")  # Đăng nhập
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)  # Thêm sản phẩm vào giỏ

        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bl/cart.html")
        self.assertContains(response, self.product.body)  # Kiểm tra có sản phẩm trong giỏ

    # 5️⃣ Kiểm tra xóa sản phẩm khỏi giỏ hàng
    def test_delete_from_cart_view(self):
        self.client.login(username="testuser", password="testpassword")  # Đăng nhập
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)

        response = self.client.post(reverse('delete', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirect

        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())  # Kiểm tra sản phẩm đã bị xóa

    # 6️⃣ Kiểm tra tìm kiếm sản phẩm
    def test_search_view(self):
        response = self.client.get(reverse('bl') + "?q=test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.body)  # Kiểm tra sản phẩm có trong kết quả tìm kiếm
