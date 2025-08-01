from django.shortcuts import render, redirect, get_object_or_404
from .models import Homework
from .forms import HomeworkForm
from django.contrib.auth.decorators import login_required

@login_required
def homework_list(request):
    homeworks = Homework.objects.filter(user=request.user)
    return render(request, 'homework/homework_list.html', {'homeworks': homeworks,  'first_name': request.user.first_name})

@login_required
def add_homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.user = request.user
            homework.save()
            return redirect('homework_list')
    else:
        form = HomeworkForm()
    return render(request, 'homework/homework_form.html', {'form': form,  'first_name': request.user.first_name})

@login_required
def update_homework(request, pk):
    homework = get_object_or_404(Homework, pk=pk, user=request.user)
    form = HomeworkForm(request.POST or None, instance=homework)
    if form.is_valid():
        form.save()
        return redirect('homework_list')
    return render(request, 'homework/homework_form.html', {'form': form,  'first_name': request.user.first_name})

@login_required
def delete_homework(request, pk):
    homework = get_object_or_404(Homework, pk=pk, user=request.user)
    if request.method == 'POST':
        homework.delete()
        return redirect('homework_list')
    return render(request, 'homework/homework_confirm_delete.html', {'homework': homework, 'first_name': request.user.first_name})

