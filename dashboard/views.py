from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views he
from .AI_agent.ai_main import main_generate
from django.conf import settings
import os


@login_required
def dashboard(request):


    return render(request,"dashboard/dashboard.html",{'first_name': request.user.first_name })


def story_generator(request):
    static_dir = os.path.join(settings.BASE_DIR, "static")
    main_generate("A detective duck wearing a detective suit is solving a mystery of an egg", img_path=static_dir)
    return render(request, "dashboard/about.html", {'first_name': request.user.first_name})
