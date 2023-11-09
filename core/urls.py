from django.urls import path
from . import views



urlpatterns = [

    # Unauthticated Views
    path('', views.index, name="index"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('blog', views.blog, name="blog"),
    path("blog-deail/<str:pk>", views.blog_detail, name="blog-detail"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("edit-profile", views.edit_profile, name="edit-profile"),
    path('continue-registration', views.cont, name="cont"),
    path('ongoing-polls', views.poll_list, name="poll-list"),
    path('poll-detail/<int:poll_id>', views.poll_detail, name='detail'),
    path('poll-result/<int:poll_id>', views.poll_vote, name="poll-result")
    # Authenticated Views
    
]