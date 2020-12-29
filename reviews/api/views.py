from rest_framework import viewsets

from .serializers import ReviewSerializer, AnswerSerializer
from .models import Review, Answer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

from django.db.models import Count

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.values('submitted_at').order_by('submitted_at').annotate(count=Count('submitted_at'))
    serializer_class = ReviewSerializer