from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from courses.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseSerializerDetail(ModelSerializer):
    count_course_with_same_lesson = SerializerMethodField()

    def get_count_course_with_same_lesson(self, course):
        return Course.objects.filter(lesson=course.lesson).count()
    class Meta:
        model = Course
        fields = ('name', 'preview', 'description', 'count_course_with_same_lesson')



class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
