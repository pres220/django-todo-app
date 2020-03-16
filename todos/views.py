from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
    template_name = 'todo_list.html'

    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user).order_by('-date')


class TodoDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Todo
    template_name = 'todo_detail.html'

    def test_func(self):
        return self.get_object().author == self.request.user


class TodoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Todo
    fields = ('title', 'description')
    template_name = 'todo_edit.html'
    # success_url determined by Todo's get_absolute_url automatically

    def form_valid(self, form):
        # Update date timestamp
        todo = form.save(commit=False)
        todo.date = timezone.now()
        todo.save()
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().author == self.request.user


class TodoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Todo
    template_name = 'todo_delete.html'
    success_url = reverse_lazy('todo_list')

    def test_func(self):
        return self.get_object().author == self.request.user


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todo_new.html'
    fields = ('title', 'description')
    # success_url determined by Todo's get_absolute_url automatically

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



