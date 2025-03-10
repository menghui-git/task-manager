from django.http import HttpResponse
from rest_framework import viewsets
# from rest_framework.response import Response

from task_manager.models import Issue
from task_manager.serializers import IssueSerializer

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# TODO: Login

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()  # TODO: non archived, by project
    serializer_class = IssueSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]
