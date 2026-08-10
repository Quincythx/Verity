from rest_framework import generics
from .models import Technology, HypeSnapshot, DemandSnapshot
from .serializers import TechnologySerializer, HypeSnapshotSerializer, DemandSnapshotSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny


class TechnologyListView(generics.ListCreateAPIView):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

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

class GapAnalysisView(APIView):
    def get(self, request):
        results = []

        for technology in Technology.objects.all():
            hype_snapshots = HypeSnapshot.objects.filter(technology=technology).order_by('date')
            demand_snapshots = DemandSnapshot.objects.filter(technology=technology).order_by('date')

            if hype_snapshots.count() < 2 or demand_snapshots.count() < 2:
                results.append({
                    'technology': technology.name,
                    'status': 'insufficient data',
                })
                continue

            hype_trend = self.calculate_trend(hype_snapshots, 'mentions_count')
            demand_trend = self.calculate_trend(demand_snapshots, 'job_mentions_count')
            gap_score = round(demand_trend - hype_trend, 2)

            results.append({
                'technology': technology.name,
                'hype_trend_percent': hype_trend,
                'demand_trend_percent': demand_trend,
                'gap_score': gap_score,
            })

        results.sort(key=lambda r: r.get('gap_score', float('-inf')), reverse=True)
        return Response(results)

    def calculate_trend(self, snapshots, field_name):
        earliest = getattr(snapshots.first(), field_name)
        latest = getattr(snapshots.last(), field_name)

        if earliest == 0:
            return 0.0

        return round(((latest - earliest) / earliest) * 100, 2)

class CompareView(APIView):
    def get(self, request):
        tech_a_id = request.query_params.get('a')
        tech_b_id = request.query_params.get('b')

        tech_a = Technology.objects.get(pk=tech_a_id)
        tech_b = Technology.objects.get(pk=tech_b_id)

        return Response({
            'technology_a': self.build_summary(tech_a),
            'technology_b': self.build_summary(tech_b),
        })

    def build_summary(self, technology):
        hype_snapshots = HypeSnapshot.objects.filter(technology=technology).order_by('date')
        demand_snapshots = DemandSnapshot.objects.filter(technology=technology).order_by('date')

        if hype_snapshots.count() < 2 or demand_snapshots.count() < 2:
            return {'technology': technology.name, 'status': 'insufficient data'}

        gap_view = GapAnalysisView()
        hype_trend = gap_view.calculate_trend(hype_snapshots, 'mentions_count')
        demand_trend = gap_view.calculate_trend(demand_snapshots, 'job_mentions_count')

        return {
            'technology': technology.name,
            'hype_trend_percent': hype_trend,
            'demand_trend_percent': demand_trend,
            'gap_score': round(demand_trend - hype_trend, 2),
        }