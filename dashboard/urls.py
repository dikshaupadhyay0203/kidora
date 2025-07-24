from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('edit-profile', views.edit_profile, name="edit"),
    path('feedback-form', views.feedback_form, name="feedback"),
    path('story-generate', views.story_generate, name="story_generate"),
    path('quiz/',views.quiz,name="quiz"),
     path('quiz/complete/', views.quiz_complete, name='quiz_complete'),

    path('user-profile', views.user_profile, name="user_profile"),
]

