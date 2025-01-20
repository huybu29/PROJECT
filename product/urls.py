from django.urls import path
from . import views   
urlpatterns=[
  path('', views.PostListViews.as_view(), name='bl'), 
  path('<int:pk>/', views.post, name='product'),

]