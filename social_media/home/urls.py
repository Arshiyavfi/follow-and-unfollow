from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeClass.as_view(), name='home'),
    path('post/<int:post_id>/<slug:post_slug>', views.PostDetailView.as_view(), name = 'post_detail'),
    path('post/delete/<int:post_id>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/update/<int:post_id>/', views.UserUpdateView.as_view(), name='post_update'),
    path('post/create/', views.UserCreateView.as_view(), name='post_create'),
]
