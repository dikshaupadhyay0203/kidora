from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('edit-profile', views.edit_profile, name="edit"),
    path('feedback-form', views.feedback_form, name="feedback"),
    path('story-generate', views.story_generate, name="story_generate"),
    path('rhyme-generator/', views.rhyme_generator, name='rhyme_generator'),
    path('ask-buddy/', views.ask_buddy, name='ask_buddy'),
    path('quiz/',views.quiz,name="quiz"),
    path('quiz/complete/', views.quiz_complete, name='quiz_complete'),
    path('progress-level/', views.progress_level, name='progress_level'),
    path('user-profile', views.user_profile, name="user_profile"),
    path('faq/', views.faq, name='faq'),
    path('forest/',views.forest,name="forest"),
]

