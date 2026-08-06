from django.db import models

# Create your models here.
class Technology(models.Model):
    CATEGORY_CHOICES = [
        ('language', 'Language'),
        ('framework', 'Framework'),
        ('tool', 'Tool'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HypeSnapshot(models.Model):
    technology = models.ForeignKey(
        Technology,
        on_delete=models.CASCADE,
        related_name='hype_snapshots'
    )
    date = models.DateField()
    mentions_count = models.IntegerField()
    source = models.CharField(max_length=50, default='github')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['technology', 'date', 'source'],
                name='unique_hype_snapshot_per_day'
            )
        ]

    def __str__(self):
        return f"{self.technology.name} - {self.date} - {self.mentions_count}"


class DemandSnapshot(models.Model):
    technology = models.ForeignKey(
        Technology,
        on_delete=models.CASCADE,
        related_name='demand_snapshots'
    )
    date = models.DateField()
    job_mentions_count = models.IntegerField()
    country = models.CharField(max_length=100, null=True, blank=True)
    source = models.CharField(max_length=50, default='iafrica')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['technology', 'date', 'source'],
                name='unique_demand_snapshot_per_day'
            )
        ]

    def __str__(self):
        return f"{self.technology.name} - {self.date} - {self.job_mentions_count}"


class ScrapeLog(models.Model):
    SOURCE_CHOICES = [
        ('github', 'GitHub'),
        ('iafrica', 'iAfrica'),
    ]
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    message = models.TextField(blank=True)
    run_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} - {self.status} - {self.run_at}"
