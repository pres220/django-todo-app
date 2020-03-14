from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, TemplateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Todo


class HomePageView(TemplateView):
    template_name = 'home.html'


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    context_object_name = 'todo_list'
    ordering = ['-date']
    template_name = 'todo_list.html'

    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user)


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todo_detail.html'


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ('title', 'body')
    template_name = 'todo_edit.html'

    def form_valid(self, form):
        # Update date timestamp
        todo = form.save(commit=False)
        todo.date = timezone.now()
        todo.save()
        return super().form_valid(form)


class TodoDeleteView(DeleteView):
    model = Todo
    template_name = 'todo_delete.html'
    success_url = reverse_lazy('todo_list')


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todo_new.html'
    fields = ('title', 'body')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


