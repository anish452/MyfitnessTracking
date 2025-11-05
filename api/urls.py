from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, register
from django.urls import path

router = DefaultRouter()
router.register('activities', ActivityViewSet, basename='activity')

urlpatterns = [
    path('auth/register/', register, name='register'),
]

urlpatterns += router.urls
