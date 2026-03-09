from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Feedback, Subject, Quiz, Progress, Topic, FrequentQuestion
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .AI_agent.generate_story import generate_long_story
from .AI_agent.chat_bot import generate_rhyme, ask_your_buddy
import os
import json
import urllib.request
import urllib.error
from accounts.models import UserProfile
from django.db.models import Avg, F, Prefetch
from dotenv import load_dotenv

load_dotenv()


def record_frequent_question(query_text: str):
    normalized_query = " ".join((query_text or "").split()).strip()
    if not normalized_query:
        return

    normalized_query = normalized_query[:300]
    existing_question = FrequentQuestion.objects.filter(question_text__iexact=normalized_query).first()

    if existing_question:
        existing_question.search_count = F('search_count') + 1
        existing_question.save(update_fields=['search_count', 'last_searched'])
    else:
        FrequentQuestion.objects.create(question_text=normalized_query)


def build_local_story_paragraphs(user_prompt: str):
    prompt = (user_prompt or "your idea").strip()
    return (
        f"One bright morning, a young explorer began a magical journey about {prompt}. "
        "The sky shimmered, the wind whispered kind secrets, and every step felt like a new discovery. "
        "Soon, they met friendly helpers who believed that brave hearts can solve any problem together.\n\n"
        "As the adventure grew, a tricky challenge appeared and tested their patience. "
        f"Instead of giving up, the explorer remembered why {prompt} mattered so much and tried again with courage. "
        "With teamwork, kindness, and clever thinking, they slowly turned a hard moment into a hopeful one.\n\n"
        "By sunset, the journey ended with laughter, new friendships, and a happy lesson: being kind and brave is true magic. "
        f"The explorer returned home proud, carrying a beautiful memory of {prompt} and dreaming of the next big adventure."
    )

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
            'story_text': None,
        }
        return render(request, 'dashboard/story_generator.html', context)

    if request.method == "POST":
        user_input = request.POST.get('user_input')
        if user_input:
            record_frequent_question(user_input)
            try:
                story_text = generate_long_story(user_input)
                if not story_text or not story_text.strip():
                    story_text = build_local_story_paragraphs(user_input)

                context = {
                    'user_input': user_input,
                    'first_name': request.user.first_name,
                    'story_text': story_text,
                }
                return render(request, 'dashboard/story_generator.html', context)
            except Exception as error:
                error_text = str(error)
                if 'ResourceExhausted' in error_text or '429' in error_text or 'quota' in error_text.lower():
                    return render(request, 'dashboard/story_generator.html', {
                        'user_input': user_input,
                        'first_name': request.user.first_name,
                        'story_text': build_local_story_paragraphs(user_input),
                    })
                else:
                    return render(request, 'dashboard/story_generator.html', {
                        'user_input': user_input,
                        'first_name': request.user.first_name,
                        'story_text': build_local_story_paragraphs(user_input),
                    })
                return render(request, 'dashboard/story_generator.html', {
                    'user_input': user_input,
                    'first_name': request.user.first_name,
                    'story_text': None,
                })
        else:
            messages.error(request, "Please enter a valid input.")

    return render(request, 'dashboard/story_generator.html')

@login_required
def quiz(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user, defaults={'coins': 250})
    if profile.coins == 0:
        profile.coins = 250
        profile.save(update_fields=['coins'])
    return render(request, "dashboard/quiz.html", {'user': request.user, 'coins': profile.coins})


@login_required
@require_POST
def generate_quiz_questions(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
        subject = payload.get('subject')
        topic = payload.get('topic')

        if not subject or not topic:
            return JsonResponse({'error': 'Subject and topic are required.'}, status=400)

        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            return JsonResponse({'error': 'GOOGLE_API_KEY is not configured on the server.'}, status=500)

        prompt = f"""Generate 15 multiple choice questions for {subject} - {topic} for primary school students (Class 3-8).

Requirements:
- 4 Easy questions (basic level)
- 5 Medium questions (intermediate level)
- 6 Hard questions (advanced level)
- Each question should have 4 options (A, B, C, D)
- Only one correct answer per question
- Questions should be age-appropriate and educational
- Include variety in question types

Format your response as a JSON array with this exact structure:
[
{{
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": 0,
    "difficulty": "easy"
}}
]

Make sure the correct answer index (0-3) corresponds to the right option in the array. Provide exactly 15 questions total."""

        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={google_api_key}"
        body = json.dumps({
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }).encode('utf-8')

        req = urllib.request.Request(
            api_url,
            data=body,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            gemini_data = json.loads(response.read().decode('utf-8'))

        generated_text = gemini_data["candidates"][0]["content"]["parts"][0]["text"]
        json_match_start = generated_text.find('[')
        json_match_end = generated_text.rfind(']')

        if json_match_start == -1 or json_match_end == -1:
            return JsonResponse({'error': 'Could not parse AI response JSON.'}, status=502)

        questions = json.loads(generated_text[json_match_start:json_match_end + 1])

        if not isinstance(questions, list) or len(questions) != 15:
            return JsonResponse({'error': f'Expected 15 questions, got {len(questions) if isinstance(questions, list) else 0}.'}, status=502)

        return JsonResponse({'questions': questions})

    except urllib.error.HTTPError as http_error:
        details = http_error.read().decode('utf-8') if hasattr(http_error, 'read') else str(http_error)
        return JsonResponse({'error': f'Gemini API request failed: {details}'}, status=502)
    except urllib.error.URLError as url_error:
        return JsonResponse({'error': f'Network error while contacting Gemini API: {url_error}'}, status=502)
    except (json.JSONDecodeError, KeyError, IndexError, TypeError, ValueError) as parse_error:
        return JsonResponse({'error': f'Failed to process AI response: {parse_error}'}, status=502)
    except Exception as error:
        return JsonResponse({'error': f'Unexpected server error: {error}'}, status=500)

@login_required
def quiz_complete(request):
    if request.method == 'POST':
        subject_name = request.POST.get('subject')
        topic_name = request.POST.get('topic')
        score = float(request.POST.get('score', 0) or 0)
        earned_coins = int(request.POST.get('earned_coins', 0) or 0)
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

        profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'coins': 250})
        if profile.coins == 0:
            profile.coins = 250
            profile.save(update_fields=['coins'])
        profile.coins = F('coins') + max(0, earned_coins)
        profile.save()
        
        return redirect('quiz')
    return redirect('quiz')

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
            record_frequent_question(user_input)
            try:
                rhyme = generate_rhyme(user_input)
            except Exception as error:
                error_text = str(error)
                if 'ResourceExhausted' in error_text or '429' in error_text or 'quota' in error_text.lower():
                    messages.error(request, "AI quota reached. Please try again in a bit or switch to a lower-cost Gemini model in .env.")
                else:
                    messages.error(request, f"Rhyme generation failed: {error}")
                return render(request, 'dashboard/rhyme_generator.html', {
                    'user_input': user_input,
                    'rhyme': None,
                    'first_name': request.user.first_name,
                })
            context = {
                'user_input': user_input,
                'rhyme': rhyme,
                'first_name': request.user.first_name,
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
            'response': None,
            'first_name': request.user.first_name,
        }
        return render(request, 'dashboard/ask_buddy.html', context)

    if request.method == "POST":
        user_input = request.POST.get('user_input')
        if user_input:
            record_frequent_question(user_input)
            try:
                response = ask_your_buddy(user_input)
            except Exception as error:
                error_text = str(error)
                if 'ResourceExhausted' in error_text or '429' in error_text or 'quota' in error_text.lower():
                    messages.error(request, "AI quota reached. Please try again in a bit or switch to a lower-cost Gemini model in .env.")
                else:
                    messages.error(request, f"Buddy request failed: {error}")
                return render(request, 'dashboard/ask_buddy.html', {
                    'user_input': user_input,
                    'response': None,
                    'first_name': request.user.first_name,
                })
            context = {
                'user_input': user_input,
                'response': response,
                'first_name': request.user.first_name,
            }
            return render(request, 'dashboard/ask_buddy.html', context)
        else:
            messages.error(request, "Please enter a valid input.")

    return render(request, 'dashboard/ask_buddy.html', {'first_name': request.user.first_name})

@login_required
def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user, defaults={'coins': 250})
    if profile.coins == 0:
        profile.coins = 250
        profile.save(update_fields=['coins'])
    user = request.user
    
    # Calculate overall quiz performance
    user_quizzes = Quiz.objects.filter(user=user)
    overall_average = user_quizzes.aggregate(Avg('score'))['score__avg'] or 0
    total_quizzes = user_quizzes.count()
    latest_quiz = user_quizzes.order_by('-completed_at').first()
    last_score = latest_quiz.score if latest_quiz else 0

    if total_quizzes == 0:
        progress_message = "Take your first quiz to start your adventure progress!"
    elif overall_average >= 85:
        progress_message = "Amazing progress! You're mastering your jungle adventure."
    elif overall_average >= 60:
        progress_message = "Great work! Keep practicing to level up even faster."
    else:
        progress_message = "Good start! Try a few more quizzes to boost your progress."
    
    # For the progress ring animation
    circumference = 2 * 3.14159 * 32  # Corresponds to the radius in the SVG
    stroke_dasharray_value = (overall_average / 100) * circumference
    
    context = {
        'coins': profile.coins,
        'first_name': request.user.first_name,
        'overall_average': overall_average,
        'total_quizzes': total_quizzes,
        'last_score': last_score,
        'progress_message': progress_message,
        'circumference': circumference,
        'stroke_dasharray_value': stroke_dasharray_value,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def faq(request):
    frequent_questions = FrequentQuestion.objects.order_by('-search_count', '-last_searched')[:10]
    return render(request, 'dashboard/faq.html', {
        'frequent_questions': frequent_questions,
        'first_name': request.user.first_name,
    })

@login_required
def forest(request):
    return render(request,'dashboard/forest.html',context={ 'first_name': request.user.first_name})