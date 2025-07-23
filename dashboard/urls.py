from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('edit-profile', views.edit_profile, name="edit"),
    path('story/', views.story_generator, name="story_generator"),
]

