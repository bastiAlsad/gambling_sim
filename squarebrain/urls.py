# urls.py
from django.urls import path
from squarebrain_app import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('ranking/', views.get_ranking, name='ranking'),
    path('update-score/', views.update_highscore, name='update_score'),
]
