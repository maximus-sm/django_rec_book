from django.urls import path

from . import views
from health.views import liveness, readiness

urlpatterns = [
    path("liveness/", views.liveness, name="liveness_check"),
    path("readiness/", views.readiness, name="readiness_check"),
]
