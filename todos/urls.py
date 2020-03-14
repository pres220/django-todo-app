from django.urls import path
from .views import (
    TodoListView,
    TodoDetailView,
    TodoUpdateView,
)


urlpatterns = [
    #path('signup/', SignUpView.as_view(), name='signup'),
    path('', TodoListView.as_view(), name='todo_list'),
    path('<int:pk>', TodoDetailView.as_view(), name='todo_detail'),
    path('<int:pk>/edit', TodoUpdateView.as_view(), name='todo_edit'),
]


