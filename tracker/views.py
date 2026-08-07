from rest_framework import generics
from .models import Technology, HypeSnapshot, DemandSnapshot
from .serializers import TechnologySerializer, HypeSnapshotSerializer, DemandSnapshotSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class TechnologyListView(generics.ListAPIView):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer

class TechnologyDetailView(generics.RetrieveAPIView):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer

class TechnologyHistoryView(APIView):
    def get(self, request, pk):
        technology = Technology.objects.get(pk=pk)
        hype_snapshots = HypeSnapshot.objects.filter(technology=technology)
        demand_snapshots = DemandSnapshot.objects.filter(technology=technology)

        hype_data = HypeSnapshotSerializer(hype_snapshots, many=True).data
        demand_data = DemandSnapshotSerializer(demand_snapshots, many=True).data

        return Response({
            'technology': technology.name,
            'hype_history': hype_data,
            'demand_history': demand_data,
        })