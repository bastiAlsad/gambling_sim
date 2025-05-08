# urls.py
from django.urls import path
from gambling_sim_app import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('ranking/', views.get_ranking, name='ranking'),
    path('update-score/', views.update_coins, name='update_score'),
]
