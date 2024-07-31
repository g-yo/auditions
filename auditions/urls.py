from django.urls import path
from .views import *
from django.contrib import admin
from .import views
urlpatterns = [
    path('', movie_list, name='movie_list'),
    path('movie/<int:pk>/', movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/apply/', apply_for_movie, name='apply_for_movie'),
    path('add/', movie_add, name='movie_add'),
    path('success/', application_success, name='application_success'),
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('userlogin/', views.userlogin, name='userlogin'),  # This should match the view function name
    path('logout/', user_logout, name='user_logout'),
    path('profile/', user_profile, name='user_profile'),

]
