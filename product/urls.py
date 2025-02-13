from django.urls import path
from . import views   
urlpatterns=[
  path('', views.list, name='bl'), 
  path('<int:pk>/', views.post, name='product'),
  path('cart/',views.cart_view,name='cart'),
  path("add-to-cart/<int:pk>/", views.add_to_cart, name="add_to_cart"),
  path('cart/delete/<int:pk>',views.delete_from_cart,name="delete"),
  path('cart/buy/<int:pk>',views.buy,name="buy"),
  path('category/<int:category_id>',views.list,name="product_by_filter"),
  path("order-success/<int:order_id>/", views.order_success, name="order_success"),
  path("order-success/", views.order, name="order")
  ]