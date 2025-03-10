from django.db import models
from django.contrib.auth.models import User as DjangoUser, Group as DjangoGroup

class User(DjangoUser):
    user_id = models.AutoField(primary_key=True)
    avatar = models.FileField(null=True, blank=True)


class Group(DjangoGroup):
    group_id = models.AutoField(primary_key=True)


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_key = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    icon = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ProjectAccess(models.Model):
    ROLES = {
        1: "Administrators",
        2: "Members",
        3: "Viewers",
    }
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLES)


class Filter(models.Model):
    filter_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    query = models.CharField(max_length=150)


class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)


class Label(models.Model):
    label_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)


class Issue(models.Model):

    class IssueTypes(models.IntegerChoices):
        EPIC = 1
        TASK = 2
        SUBTASK = 3

    class Priorities(models.IntegerChoices):
        HIGHEST = 1 
        HIGH = 2
        MEDIUM = 3
        LOW = 4
        LOWEST = 5

    # PRIORITYES = {
    #     1: 'Highest',
    #     2: 'High',
    #     3: 'Medium',
    #     4: 'Low',
    #     5: 'Lowest',
    # }
    
    issue_id = models.AutoField(primary_key=True)
    serial_number = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    issue_type = models.PositiveSmallIntegerField(choices=IssueTypes)
    summary = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey("Issue", null=True, blank=True, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name="issues", null=True, blank=True, on_delete=models.SET_NULL)
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)
    labels = models.ManyToManyField(Label, blank=True)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.PositiveSmallIntegerField(choices=Priorities, default=Priorities.MEDIUM)
    watchers = models.ManyToManyField(User, related_name="watching_issues", through="WatchList")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived_at = models.DateTimeField(null=True, blank=True)


class WatchList(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    commentor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
