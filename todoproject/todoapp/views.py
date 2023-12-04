from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from .forms import TodoForm
from .models import Task

from django.shortcuts import render, redirect


# Create your views here.
def add(request):
    task = Task.objects.all()
    if request.method == "POST":
        name = request.POST.get('task', '')
        priority = request.POST.get('priority', '')
        date = request.POST.get('date', '')
        task1 = Task(name=name, priority=priority, date=date)
        task1.save()
    return render(request, 'home.html', {'task': task})


def delete(request, taskid):
    task = Task.objects.get(id=taskid)
    if request.method == "POST":
        task.delete()
        return redirect('/')
    return render(request, 'delete.html')


def update(request, taskid):
    task = Task.objects.get(id=taskid)
    f = TodoForm(request.POST or None, instance=task)
    if f.is_valid():
        f.save()
        return redirect('/')

    return render(request, 'edit.html', {'f': f, 'task': Task})


class TaskListview(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'task'


class TaskDetailview(DetailView):
    model = Task
    template_name = 'details.html'
    context_object_name = 'task'


class TaskUpdateview(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name', 'priority', 'date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail', kwargs={'pk': self.object.id})


class TaskDeleteview(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url=reverse_lazy('cbvhome')
