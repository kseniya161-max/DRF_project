from datetime import timedelta

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, request, status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
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
    CourseSerializerDetail,
    SerializerMethodField,
    SerializerSubscribtion,
)
from .tasks import send_course_update_email
from users.tasks import check_user_activity
from users.permissions import IsModerator, IsOwner
from drf_yasg.utils import swagger_auto_schema
from courses.models import Course, Lesson, Subscription


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
        "name",
        "owner",
        "lessons__title",
    )

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of courses",
        responses={200: CourseSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new course",
        request_body=CourseSerializer,
        responses={201: CourseSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific course",
        responses={200: CourseSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific course",
        request_body=CourseSerializer,
        responses={200: CourseSerializer},
    )
    def perform_update(self, serializer):
        course = self.get_object()
        prev_updated_at = course.updated_at
        course = serializer.save()
        now = timezone.now()
        time_since_update = now - prev_updated_at

        if time_since_update > timedelta(seconds=10):
            print("отправка письма после обновления")
            send_course_update_email.delay(course.id)

    @swagger_auto_schema(
        operation_description="Delete a specific course", responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseSerializerDetail
        return CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Course.objects.filter(owner=self.request.user)
        return Course.objects.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        ~IsModerator,
        IsAuthenticated,
    )

    @swagger_auto_schema(
        operation_description="Create a new lesson",
        request_body=LessonSerializer,
        responses={201: LessonSerializer},
    )
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.none()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LessonsPaginator

    @swagger_auto_schema(
        operation_description="Retrieve a list of lessons",
        responses={200: LessonSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.none()


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )

    @swagger_auto_schema(
        operation_description="Retrieve a specific lesson",
        responses={200: LessonSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.none()


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )

    @swagger_auto_schema(
        operation_description="Update a specific lesson",
        request_body=LessonSerializer,
        responses={200: LessonSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.none()


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModerator)

    @swagger_auto_schema(
        operation_description="Delete a specific lesson", responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.none()


class SubscriptionListAPIView(APIView):
    queryset = Subscription.objects.all()
    serializer_class = SerializerSubscribtion
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Subscribe or unsubscribe from a course",
        request_body=SerializerSubscribtion,
        responses={200: "Subscription updated"},
    )
    def post(self, *args, **kwargs):
        print("Метод POST вызван")
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"

        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Новая подписка добавлена"
        return Response({"message": message}, status=status.HTTP_200_OK)
