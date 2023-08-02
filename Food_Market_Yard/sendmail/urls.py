from .views import AppointmentView
from django.urls import path


urlpatterns = [
    path('', AppointmentView.as_view()),
]
