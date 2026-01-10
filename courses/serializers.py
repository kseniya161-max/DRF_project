from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from courses.models import Course, Lesson, Subscription
from courses.validators import link_validator


class LessonSerializer(ModelSerializer):
    courses = SerializerMethodField()
    link = serializers.CharField(validators=[link_validator])

    def get_courses(self, lesson):
        return [course.name for course in Course.objects.filter(lessons=lesson)]

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = "__all__"


class CourseSerializerDetail(ModelSerializer):
    count_course_with_same_lesson = SerializerMethodField()
    lessons = LessonSerializer()

    def get_count_course_with_same_lesson(self, course):
        return Course.objects.filter(lessons=course.lesson).count()

    class Meta:
        model = Course
        fields = (
            "name",
            "preview",
            "description",
            "count_course_with_same_lesson",
            "lessons",
        )


class SerializerSubscribtion(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
