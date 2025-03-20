from rest_framework import serializers

from task_manager.models import Project, Issue, Label, Status, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'avatar']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['status_id', 'name']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['label_id', 'name']


class PrioritySerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'code': instance,
            'name': Issue.Priorities(instance).name.capitalize()
        }


class IssueSerializer(serializers.ModelSerializer):
    assignee = UserSerializer()
    status = StatusSerializer()
    priority = PrioritySerializer()
    labels = LabelSerializer(many=True)
    # TODO: is_watching

    class Meta:
        model = Issue
        fields = '__all__'  # exclude watchers

    def create(self, validated_data):
        new_data = validated_data.copy() 

        # project
        project_id = new_data.pop('project_id')
        project = Project.objects.get(project_id=project_id)
        new_data['project'] = project

        # serial_number
        project_id = new_data['project'].project_id
        serial_number = Issue.objects.get_latest_serial_number(project_id) + 1
        new_data['serial_number'] = serial_number

        # TODO: add creator to watcher list
        assignee = new_data.get('assignee')
        if assignee:
            new_data['watchers'] = [assignee]

        return super().create(new_data)

    def to_internal_value(self, data):
        new_data = data.copy()
        
        assignee_id = new_data.pop('assignee_id', None)
        status_id = new_data.pop('status_id', None)
        label_ids = new_data.pop('label_ids', None)

        if assignee_id:
            assignee = User.objects.get(user_id=assignee_id)
            new_data['assignee'] = assignee

        if status_id:
            status = Status.objects.get(status_id=status_id)
            new_data['status'] = status

        if label_ids:
            labels = Label.objects.filter(label_id__in=label_ids)
            new_data['labels'] = labels

        return new_data