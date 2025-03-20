from rest_framework import viewsets

from task_manager.models import Issue
from task_manager.serializers import IssueSerializer

# TODO: Login

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()  # TODO: firter non-archived issues by project
    serializer_class = IssueSerializer
    # permission_classes = []
