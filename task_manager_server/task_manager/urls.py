from django.urls import path

from task_manager import views

urlpatterns = [
    path('issue/', views.IssueViewSet.as_view({'get': 'list'})),
    path("", views.index, name="index"),
]