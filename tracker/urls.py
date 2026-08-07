from django.urls import path
from .views import TechnologyListView

urlpatterns = [
    path('technologies/', TechnologyListView.as_view(), name='technology-list'),
]