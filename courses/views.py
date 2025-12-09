from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, request, status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView, get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from courses.models import Course, Lesson, Subscription
from courses.paginators import CoursesPaginator, LessonsPaginator
from courses.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseSerializerDetail, SerializerMethodField,
)
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursesPaginator
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = (
        "course",
        "lessons__title",
    )
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseSerializerDetail
        return CourseSerializer

    # def get_permissions(self):
    #     if self.action == "create":
    #         self.permission_classes = ~IsModerator
    #     elif self.action in ["update", "retrieve"]:
    #         self.permission_classes = (IsModerator | IsOwner,)
    #     elif self.action == "destroy":
    #         self.permission_classes = (~IsModerator | IsOwner,)
    #     return super().get_permissions()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]  # например, только аутентифицированные пользователи
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        else:
            self.permission_classes = [IsAuthenticated]  # для всех остальных действий

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context



class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        ~IsModerator,
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LessonsPaginator

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModerator)

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)


class SubscriptionListAPIView(APIView):
    queryset = Subscription.objects.all()
    serializer_class = SerializerMethodField
    permission_classes = [IsAuthenticated]


    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Новая подписка добавлена'
        return Response({'message': message}, status=status.HTTP_200_OK)





