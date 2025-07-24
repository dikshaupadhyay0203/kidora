from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('edit-profile', views.edit_profile, name="edit"),
    path('feedback-form', views.feedback_form, name="feedback"),
]

