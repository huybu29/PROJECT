from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from product.views import search
urlpatterns=[
  path('',views.index),
  path('register/', views.register, name='register'),
  path( 'login/',auth_views.LoginView.as_view(template_name="pages/login.html"), name="login"),
  path( 'logout/',auth_views.LogoutView.as_view(next_page="/blog"), name='logout'),
  path("products/", search, name="product_list"),
]