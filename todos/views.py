from django.views.generic import CreateView, ListView, TemplateView, DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Todo


class HomePageView(TemplateView):
    template_name = 'home.html'


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'signup.html'


class TodoListView(ListView):
    model = Todo
    template_name = 'todo_list.html'


class TodoDetailView(DetailView):
    model = Todo
    template_name = 'todo_detail.html'


class TodoUpdateView(UpdateView):
    model = Todo
    fields = ('title', 'body')
    template_name = 'todo_edit.html'

    def form_valid(self, form):
        # Update date timestamp
        todo = form.save(commit=False)
        todo.date = timezone.now()
        todo.save()
        return super().form_valid(form)

