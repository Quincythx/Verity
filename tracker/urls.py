from django.urls import path
from .views import TechnologyListView, TechnologyDetailView

urlpatterns = [
    path('technologies/', TechnologyListView.as_view(), name='technology-list'),
    path('technologies/<int:pk>/', TechnologyDetailView.as_view(), name='technology-detail'),
]