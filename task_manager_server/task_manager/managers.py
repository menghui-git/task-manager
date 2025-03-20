from django.db import models

class IssueManager(models.Manager):
    def get_latest_serial_number(self, project_id):  # TODO: ensure consistency
        try:
            return super().get_queryset().filter(project__project_id=project_id).values_list('serial_number', flat=True).latest('created_at')
        except self.model.DoesNotExist:
            return 0