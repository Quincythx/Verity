from django.urls import path
from .views import TechnologyListView, TechnologyDetailView, TechnologyHistoryView

urlpatterns = [
    path('technologies/', TechnologyListView.as_view(), name='technology-list'),
    path('technologies/<int:pk>/', TechnologyDetailView.as_view(), name='technology-detail'),
    path('technologies/<int:pk>/history/', TechnologyHistoryView.as_view(), name='technology-history'),
]