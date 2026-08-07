from rest_framework import generics
from .models import Technology
from .serializers import TechnologySerializer


class TechnologyListView(generics.ListAPIView):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer