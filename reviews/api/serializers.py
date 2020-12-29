from rest_framework import serializers

from .models import Review, Question, Answer, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['text']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['review','question','choice']

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
        answers = Answer.objects.filter(review__submitted_at=instance['submitted_at'])
        answer_serializer = AnswerSerializer(answers, many=True)
        return answer_serializer.data
        