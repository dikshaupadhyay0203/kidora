from django.urls import path
from . import views

urlpatterns = [
    path('', views.homework_list, name='homework_list'),
    path('add/', views.add_homework, name='add_homework'),
    path('update/<int:pk>/', views.update_homework, name='update_homework'),
    path('delete/<int:pk>/', views.delete_homework, name='delete_homework'),
]
