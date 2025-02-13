from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('get_title/', views.get_title, name='get_title'),
    path('quiz/', views.quiz, name="quiz"),
    path('check_answer/', views.check_answer, name='check_answer'),
    path('quiz_results/', views.quiz_results, name='quiz_results'),
    path('questions/', views.questions, name="questions"),
]
