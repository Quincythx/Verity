from rest_framework import serializers
from .models import Technology, HypeSnapshot, DemandSnapshot, ScrapeLog


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ['id', 'name', 'category', 'created_at']

class HypeSnapshotSerializer(serializers.ModelSerializer):
    technology = serializers.StringRelatedField()

    class Meta:
        model = HypeSnapshot
        fields = ['id', 'technology', 'date', 'mentions_count', 'source']


class DemandSnapshotSerializer(serializers.ModelSerializer):
    technology = serializers.StringRelatedField()

    class Meta:
        model = DemandSnapshot
        fields = ['id', 'technology', 'date', 'job_mentions_count', 'country', 'source']


class ScrapeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapeLog
        fields = ['id', 'source', 'status', 'message', 'run_at']