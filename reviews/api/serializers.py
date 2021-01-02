from rest_framework import serializers
from .models import Review, Question, Answer, Choice, Day
from django.db.models import Count, F

class DaySerializer(serializers.ModelSerializer):
    submitted_at = serializers.SerializerMethodField(method_name='get_date')
    count = serializers.SerializerMethodField(method_name='get_count')
    answers = serializers.SerializerMethodField(method_name='get_answers')
    class Meta:
        model = Day
        fields = ['submitted_at', 'count', 'answers']
    def get_count(self, instance):
        return len(instance._prefetched_objects_cache['reviews'])
    def get_date(self, instance):
        return instance.date
    def get_answers(self, instance):
        q = instance._prefetched_objects_cache['reviews']
        answers_query = Answer.objects.none()
        for q_set in q:
            answers_query = answers_query | q_set.answers.all()
        answers_query = answers_query.values('choice__text').annotate(choice=F('choice__text'),count=Count('choice__text')).values('choice','count')
        return answers_query