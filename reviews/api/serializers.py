from rest_framework import serializers
from .models import Review, Question, Answer, Choice
from django.db.models import Count

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['text']

class AnswerSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(method_name='get_count')
    qustion = serializers.SerializerMethodField(method_name='get_question')
    choice = serializers.SerializerMethodField(method_name='get_choice')
    
    class Meta:
        model = Answer
        fields = ['qustion','choice','count']
    
    def get_count(self, instance):
        return instance['count']
    def get_question(self, instance):
        return instance['question__text']
    def get_choice(self, instance):
        return instance['choice__text']
    
    

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text']

class ReviewSerializer(serializers.ModelSerializer):
    
    answers = serializers.SerializerMethodField(method_name='get_answers')
    count = serializers.SerializerMethodField(method_name='get_count')
    
    class Meta:
        model = Review
        fields = ('submitted_at', 'answers', 'count')

    def get_count(self, instance):
        return instance['count']
        
    def get_answers(self, instance):
        answers = Answer.objects.filter(review__submitted_at=instance['submitted_at']).values('question__text','choice__text').annotate(count=Count('choice__text'))
        answer_serializer = AnswerSerializer(answers, many=True)
        return answer_serializer.data
        