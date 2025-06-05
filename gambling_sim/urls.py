# urls.py
from django.urls import path
from gambling_sim_app import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('get-ranking/', views.get_ranking, name='get-ranking'),
    path('update-coins/', views.update_coins, name='update-coins'),
]
