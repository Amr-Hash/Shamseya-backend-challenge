from rest_framework import viewsets
from django.db.models import Count
from .serializers import ReviewSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import BasicAuthentication
from .models import Review, Answer


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.values('submitted_at')

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        from_date = self.request.query_params.get('from', None)
        to_date = self.request.query_params.get('to', None)
        if from_date:
            self.queryset = self.queryset.filter(submitted_at__gte=from_date)
        if to_date:
            self.queryset = self.queryset.filter(submitted_at__lte=to_date)
        self.queryset = self.queryset.order_by('submitted_at').annotate(count=Count('submitted_at'))
        return self.queryset