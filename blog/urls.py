from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blogHome'),
    path('blogpost/<slug:slug>/', views.blogpost, name='blog_detail'),  # ✅ This name must match 'blog_detail'
]
