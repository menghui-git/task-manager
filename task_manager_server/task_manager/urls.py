from django.urls import path

from task_manager import views

urlpatterns = [
    path('issue/', views.IssueViewSet.as_view({'get': 'list', 
                                               'post': 'create'})),
    path('issue/<int:pk>', views.IssueViewSet.as_view({'get':'retrieve', 
                                                       'patch': 'partial_update', 
                                                       'delete': 'destroy'})),
]