from rest_framework import serializers

from task_manager.models import Issue, Label, Status, User


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
        fields = '__all__'


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

    class Meta:
        model = Issue
        fields = '__all__'

    def create(self, validated_data):
        return Issue.objects.create(**validated_data)