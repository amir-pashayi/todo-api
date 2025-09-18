from rest_framework import serializers
from .models import Task, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','title','description')
        read_only_fields = ('id',)

    def create(self, validated_data):
        return Category.objects.create(user=self.context['request'].user, **validated_data)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.user = self.context['request'].user
        instance.save()
        return instance

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id','title','description','start_date','end_date','flag','category','is_complete')
        read_only_fields = ('id','start_date','is_complete')

    def validate(self, attrs):
        end = attrs.get('end_date')
        start = None
        if self.instance:
            start = self.instance.start_date
        if end and start and end < start:
            raise serializers.ValidationError({'end_date': 'must be after start_date'})
        return attrs

    def create(self, validated_data):
        return Task.objects.create(user=self.context['request'].user, **validated_data)


class IdsPayloadSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False,
        help_text="List of Task IDs"
    )

    def validate_ids(self, value):
        return list(dict.fromkeys(value))[:500]