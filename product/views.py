from django.shortcuts import render,get_object_or_404
from .models import Product, Cart, CartItem
from django.views.generic import ListView, DetailView
from product.forms import CommentForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.
def list(request):
  data={'Products':Product.objects.all().order_by("-date")}
  return render(request, 'bl/bl.html', data)
class PostListViews(ListView):
  queryset=Product.objects.all().order_by("-date")
  template_name='bl/bl.html'
  context_object_name='Product'
  paginate_by=4
def post(request, pk):
  product = get_object_or_404(Product, pk=pk)
  form = CommentForm()
  if request.method=='POST':
    form=CommentForm(request.POST, author=request.user, product=product)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(request.path)
  return render(request,"bl/post.html",{"product":product,"form":form})
class PostDetaiView(DetailView):  
  model = Product
  template_name='bl/post.html'
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Kiểm tra nếu sản phẩm đã tồn tại trong giỏ
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'cart_detail.html', {'cart': cart})