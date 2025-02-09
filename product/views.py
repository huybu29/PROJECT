from django.shortcuts import render,get_object_or_404,redirect
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


def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = cart.total_price()
    tax=cart.tax()
    return render(request, "bl/cart.html", {"cart_items": cart_items, "total_price": total_price,"tax":tax})

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


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))  # Lấy số lượng từ form
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity  # Cộng dồn số lượng
        cart_item.save()
    return HttpResponseRedirect('/')
def buy(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
  
       
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
    cart_item.save()
    return HttpResponseRedirect('/blog/cart')
def delete_from_cart(request,pk):
    cart=get_object_or_404(Cart,user=request.user)
    cart_item= get_object_or_404(CartItem,cart=cart,product_id=pk)

    cart_item.delete()
    return HttpResponseRedirect('/')
def search(request):
    query = request.GET.get("q") 
    if query:
        products = Product.objects.filter(title__icontains=query)  
    else:
        products = Product.objects.all()  

    return render(request, "bl/bl.html", {"Products": products, "query": query})