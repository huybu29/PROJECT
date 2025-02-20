from django.shortcuts import render,get_object_or_404,redirect
from .models import Product, Cart, CartItem,Category,Order,OrderItem
from django.views.generic import ListView, DetailView
from product.forms import CommentForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def list(request,category_id=None):
  category=Category.objects.all().order_by('id')
  if category_id:
     selected_category=Category.objects.get(id=category_id)
     product=Product.objects.filter(category=selected_category)
  else:
     selected_category=None  
     product=Product.objects.all()
  return render(request, 'bl/bl.html', {"Product":product,"Category":category,"selected-category":selected_category})

def post(request, pk):
  product = get_object_or_404(Product, pk=pk)
  form = CommentForm()
  if request.method=='POST':
    form=CommentForm(request.POST, author=request.user, product=product)    
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(request.path)
  return render(request,"bl/post.html",{"product":product,"form":form})


def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = cart.total_price()
    tax = cart.tax()

    if request.method == "POST":
        shipping_address = request.POST.get("shipping_address")

        if not shipping_address:
            messages.error(request, "Vui lòng nhập địa chỉ giao hàng.")
            return redirect("cart_view")

        # Tạo đơn hàng với địa chỉ giao hàng
        order = Order.objects.create(
            user=request.user,
            total_price=total_price + tax,
            address=shipping_address
        )

        # Chuyển sản phẩm từ giỏ hàng sang đơn hàng
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        # Xóa giỏ hàng
        cart.items.all().delete()

        return redirect("order_success", order_id=order.id)

    return render(request, "bl/cart.html", {"cart_items": cart_items, "total_price": total_price, "tax": tax})

def post(request, pk):
  product = get_object_or_404(Product, pk=pk)
  form = CommentForm()
  
  if request.method=='POST':
    form=CommentForm(request.POST, author=request.user, product=product)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(request.path)
    
  return render(request,"bl/post.html",{"product":product,"form":form})   
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Product, Cart, CartItem

def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()
    return HttpResponseRedirect('/')

def buy(request, pk):
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.save()
    return HttpResponseRedirect('/blog/cart')

def delete_from_cart(request,pk):
    cart=get_object_or_404(Cart,user=request.user)
    cart_item= get_object_or_404(CartItem,cart=cart,product_id=pk)

    cart_item.delete()
    return HttpResponseRedirect('/blog/cart')
def search(request):
      query = request.GET.get("q")
      if query:
          products = Product.objects.filter(body__icontains=query)  
      else:
          products = Product.objects.all()  

      return render(request, "bl/bl.html", {"Products": products, "query": query})

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "bl/order.html", {"order": order})
def order(request):
    order=Order.objects.all()
    return render(request,'bl/order_list.html',{"order":order})
