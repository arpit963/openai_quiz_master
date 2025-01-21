from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('quiz/', views.quiz, name="quiz"),
    path('quiz_results/', views.quiz_results, name='quiz_results'),
    path('questions/', views.questions, name="questions"),
    path('next_question/', views.next_question, name='next_question'),
    path('check_answer/', views.check_answer, name='check_answer'),
   
    # Testing url
    # path('input/', views.input_form_view, name='input_form'),
    # path('quiz/<int:question_id>/', views.quiz_view, name='quiz_view'),
]
