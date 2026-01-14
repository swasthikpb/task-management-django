from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model =Task
        fields = '__all__'
        read_only_field = ('assigned_to',)

class TaskCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model =Task
        fields = ('status', 'completion_report', 'worked_hours')

    def validate(self, data):
        if data.get('status') == 'COMPLETED':
            if not data.get('completion_report') or not data.get('worked_hours'):
                raise serializers.ValidationError(
                    "Completion report and worked hours are required."
                )
        
        return data