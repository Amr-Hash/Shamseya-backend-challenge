from rest_framework import viewsets
from django.db.models import Count, Prefetch
from .serializers import ReviewSerializer, AnswerSerializer2, DaySerializer
from rest_framework.permissions import IsAdminUser, BasePermission
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from .models import Review, Answer, Day
from .decorators import query_debugger
from rest_framework.response import Response

class IsStaffOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.is_staff)

class DayViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DaySerializer
    queryset = Day.objects.prefetch_related('reviews').all()

    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsStaffOrSuperUser]

    def get_queryset(self):
        grand_children = Prefetch('reviews__answers', queryset=Answer.objects.select_related('review','question','choice'))
        queryset = Day.objects.prefetch_related(grand_children)

        from_date = self.request.query_params.get('from', None)
        to_date = self.request.query_params.get('to', None)
        if from_date:
            self.queryset = self.queryset.filter(date__gte=from_date)
        if to_date:
            self.queryset = self.queryset.filter(date__lte=to_date)
        return queryset
    @query_debugger
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
     
class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsStaffOrSuperUser]

    serializer_class = ReviewSerializer
    queryset = Review.objects.prefetch_related('answers').values('submitted_at')
    
    def get_queryset(self):
        from_date = self.request.query_params.get('from', None)
        to_date = self.request.query_params.get('to', None)
        if from_date:
            self.queryset = self.queryset.filter(submitted_at__gte=from_date)
        if to_date:
            self.queryset = self.queryset.filter(submitted_at__lte=to_date)
        self.queryset = self.queryset.order_by('submitted_at').annotate(count=Count('submitted_at'))
        return self.queryset
    
    @query_debugger
    def list(self, request):
        queryset = self.get_queryset()
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AnswerSerializer2
    queryset = Answer.objects.select_related('review','choice','question').all()
    
    @query_debugger
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
     