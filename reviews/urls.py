from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('general_service_reviews', views.ReviewViewSet)  

urlpatterns = router.urls