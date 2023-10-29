from django.urls import path
from . import views

urlpatterns = [

    # Unauthticated Views
    path('', views.index, name="index"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('blog', views.blog, name="blog"),
    path("blog-deail/<str:pk>", views.blog_detail, name="blog-detail")


    # Authenticated Views
    
]