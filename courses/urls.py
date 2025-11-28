from rest_framework.routers import SimpleRouter
from courses.views import CourseViewSet

app_name = "courses"

router = SimpleRouter()
router.register(r"course", CourseViewSet)


urlpatterns = []
urlpatterns += router.urls
