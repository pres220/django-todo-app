from django.urls import path
from .views import (
    TodoListView,
    TodoDeleteView,
    TodoDetailView,
    TodoUpdateView,
)


urlpatterns = [
    path('', TodoListView.as_view(), name='todo_list'),
    path('<int:pk>/', TodoDetailView.as_view(), name='todo_detail'),
    path('<int:pk>/edit/', TodoUpdateView.as_view(), name='todo_edit'),
    path('<int:pk>/delete/', TodoDeleteView.as_view(), name='todo_delete'),
]


