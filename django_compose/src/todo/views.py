from django.shortcuts import render, redirect
from .models import Todo

def todo_list(request):
    todos = Todo.objects.order_by('-created_at')
    return render(request, 'todo/todo_list.html', {'todos': todos})

def todo_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Todo.objects.create(title=title)
        return redirect('todo_list')
    return render(request, 'todo/todo_create.html')
