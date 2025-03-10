from django.contrib import admin

from task_manager.models import User, Project, ProjectAccess, Filter, Status, Label, Issue, WatchList, Comment


class UserAdmin(admin.ModelAdmin):
    pass


class ProjectAdmin(admin.ModelAdmin):
    pass


class IssueAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectAccess)
admin.site.register(Filter)
admin.site.register(Status)
admin.site.register(Label)
admin.site.register(Issue, IssueAdmin)
admin.site.register(WatchList)
admin.site.register(Comment, CommentAdmin)

# python3 manage.py makemigrations task_manager
# python3 manage.py migrate
