from rest_framework import serializers

class TaskInputSerializer(serializers.Serializer):
    """
    Input ke liye simple serializer.
    Yeh model se bind nahi hai, bas JSON validate karega.
    """
    title = serializers.CharField(max_length=255)
    due_date = serializers.DateField(required=False, allow_null=True)
    estimated_hours = serializers.FloatField(
        required=False,
        allow_null=True,
        min_value=0
    )
    importance = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=10
    )
    # dependencies as list of IDs (string ya number)
    dependencies = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )


class TaskOutputSerializer(TaskInputSerializer):
    """
    Output me wahi fields + score + explanation.
    """
    score = serializers.FloatField()
    explanation = serializers.CharField()
