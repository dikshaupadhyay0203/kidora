from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Feedback, Subject, Quiz, Progress, Topic
from django.contrib import messages
from .AI_agent.ai_main import main_generate
from .AI_agent.chat_bot import generate_rhyme, ask_your_buddy
from django.conf import settings
import os
from accounts.models import UserProfile
from django.db.models import Avg, F, Prefetch

@login_required
def progress_level(request):
    user = request.user
    
    # Get all subjects
    all_subjects = Subject.objects.all()
    
    # Get subjects for which the user already has progress
    subjects_with_progress_ids = Progress.objects.filter(user=user).values_list('subject_id', flat=True)
    
    # Find subjects for which progress needs to be created
    subjects_to_create_progress_for = all_subjects.exclude(id__in=subjects_with_progress_ids)
    
    # Create progress objects in bulk
    if subjects_to_create_progress_for:
        Progress.objects.bulk_create([
            Progress(user=user, subject=subject) for subject in subjects_to_create_progress_for
        ])
    
    # Now fetch all subjects with prefetched progress
    subjects = all_subjects.prefetch_related(
        Prefetch('progress_set', queryset=Progress.objects.filter(user=user), to_attr='user_progress'),
        Prefetch('quiz_set', queryset=Quiz.objects.filter(user=user).select_related('topic'))
    )

    for subject in subjects:
        # Since we ensured progress exists, user_progress should not be empty.
        subject.progress = subject.user_progress[0]

    return render(request, 'dashboard/progress_level.html', {'subjects': subjects, 'first_name': user.first_name})

@login_required
def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'dashboard/dashboard.html', {'coins': profile.coins, 'first_name': request.user.first_name})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
          user.first_name = request.POST.get('first_name')
          user.last_name = request.POST.get('last_name')
          user.username = request.POST.get('username')
          user.email = request.POST.get('email')
          user.save()
          messages.success(request, f"User profile updated successfully")
          return redirect('dashboard')
    context = {'user': user}
    return render(request, 'dashboard/edit_profile.html', context)


@login_required
def change_password(request):
     user = request.user
     if request.method == "POST":   
          new_password = request.POST.get('password')
          user.set_password(new_password)
          user.save()
          messages.success(request, f"Password changed successfully")
          return redirect('dashboard')
     return render(request, 'dashboard/dashboard.html')

@login_required
def feedback_form(request):
     if request.method == "POST":
        feedback = Feedback(
             user = request.user,
             subject= request.POST.get('subject'),
             message = request.POST.get('message'),
             feedback_type = request.POST.get('feedback_type')
        )
        feedback.save()
        messages.success(request, f"Feedback Submitted Successfully")
        return redirect(dashboard)
     
     return render(request, 'dashboard/feedback-form.html')

@login_required
def user_profile(request):
     context = {'first_name': request.user.first_name, 'last_name': request.user.last_name, 
                'email': request.user.email, 'username': request.user.username
               }
     return render(request, 'dashboard/user-profile.html',context)

@login_required
def story_generate(request):
     if request.method == "GET":
          context = {
               'user_input': None,
               'first_name': request.user.first_name,
          }
          return render(request, 'dashboard/story_generator.html', context)

     if request.method == "POST":
          user_input = request.POST.get('user_input')
          static_dir = os.path.join(settings.BASE_DIR, "static","generated_images")
          if user_input:
               main_generate(user_input, static_dir)
               context = {
                'user_input': user_input,
                'first_name': request.user.first_name,
            }
               return render(request, 'dashboard/story_generator.html', context)
          else:
               messages.error(request, "Please enter a valid input.")
    
     return render(request, 'dashboard/story_generator.html')

@login_required
def quiz(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "dashboard/quiz.html", {'user': request.user, 'coins': profile.coins})

@login_required
def quiz_complete(request):
    if request.method == 'POST':
        subject_name = request.POST.get('subject')
        topic_name = request.POST.get('topic')
        score = float(request.POST.get('score'))
        user = request.user

        subject, _ = Subject.objects.get_or_create(name=subject_name)
        topic, _ = Topic.objects.get_or_create(name=topic_name, subject=subject)

        Quiz.objects.create(user=user, subject=subject, topic=topic, score=score)

        progress, _ = Progress.objects.get_or_create(user=user, subject=subject)
        progress.last_score = score

        # Calculate average of last 5 quizzes for the subject
        recent_quizzes = Quiz.objects.filter(user=user, subject=subject).order_by('-completed_at')[:5]
        average_score = recent_quizzes.aggregate(Avg('score'))['score__avg'] or 0
        progress.average_percentage = average_score

        # Generate suggestion based on topics with lowest average scores
        topic_averages = Quiz.objects.filter(user=user, subject=subject, topic__isnull=False).values('topic__name').annotate(average=Avg('score')).order_by('average')
        
        if topic_averages:
            min_topic = topic_averages[0]['topic__name']
            progress.suggestion = f"You seem to be struggling with {min_topic}. We suggest you to read more about it."
        
        progress.save()

        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.coins = F('coins') + 2
        profile.save()
        
        return redirect('quiz_complete')
    return redirect('quiz_complete')

@login_required
def rhyme_generator(request):
    if request.method == "GET":
        context = {
            'user_input': None,
            'rhyme': None,
             'first_name': request.user.first_name
        }
        return render(request, 'dashboard/rhyme_generator.html', context)

    if request.method == "POST":
        user_input = request.POST.get('user_input')
        if user_input:
            rhyme = generate_rhyme(user_input)
            context = {
                'user_input': user_input,
                'rhyme': rhyme
            }
            return render(request, 'dashboard/rhyme_generator.html', context)
        else:
            messages.error(request, "Please enter a valid input.")
    
    return render(request, 'dashboard/rhyme_generator.html')


@login_required
def ask_buddy(request):
     if request.method == "GET":
          context = {
               'user_input': None,
               'response': None
          }
          return render(request, 'dashboard/ask_buddy.html', context)
     
     if request.method == "POST":
          user_input = request.POST.get('user_input')
          if user_input:
               response = ask_your_buddy(user_input)
               context = {
                    'user_input': user_input,
                    'response': response
               }
               return render(request, 'dashboard/ask_buddy.html', context)
          else:
               messages.error(request, "Please enter a valid input.")
     
     return render(request, 'dashboard/ask_buddy.html')

@login_required
def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user = request.user
    
    # Calculate overall quiz performance
    overall_average = Quiz.objects.filter(user=user).aggregate(Avg('score'))['score__avg'] or 0
    
    # For the progress ring animation
    circumference = 2 * 3.14159 * 32  # Corresponds to the radius in the SVG
    stroke_dasharray_value = (overall_average / 100) * circumference
    
    context = {
        'coins': profile.coins,
        'first_name': request.user.first_name,
        'overall_average': overall_average,
        'circumference': circumference,
        'stroke_dasharray_value': stroke_dasharray_value,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def faq(request):
    return render(request, 'dashboard/faq.html')

@login_required
def forest(request):
    return render(request,'dashboard/forest.html',context={ 'first_name': request.user.first_name})