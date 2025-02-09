from django.urls import path
from . import views   
urlpatterns=[
  path('', views.PostListViews.as_view(), name='bl'), 
  path('<int:pk>/', views.post, name='product'),
  path('cart/',views.cart_view,name='cart'),
  path("add-to-cart/<int:pk>/", views.add_to_cart, name="add_to_cart"),
  path('cart/delete/<int:pk>',views.delete_from_cart,name="delete"),
  path('cart/buy/<int:pk>',views.buy,name="buy"),
  path("products/", views.search, name="product_list"),
]