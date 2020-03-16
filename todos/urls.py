from django.urls import path
from .views import (
    TodoListView,
    TodoCreateView,
    TodoDeleteView,
    TodoDetailView,
    TodoUpdateView,
)


urlpatterns = [
    path('', TodoListView.as_view(), name='todo_list'),
    path('<uuid:pk>/', TodoDetailView.as_view(), name='todo_detail'),
    path('<uuid:pk>/edit/', TodoUpdateView.as_view(), name='todo_edit'),
    path('<uuid:pk>/delete/', TodoDeleteView.as_view(), name='todo_delete'),
    path('new/', TodoCreateView.as_view(), name='todo_new'),
]


