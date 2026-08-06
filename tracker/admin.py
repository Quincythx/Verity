from django.contrib import admin
from .models import Technology, HypeSnapshot, DemandSnapshot, ScrapeLog

admin.site.register(Technology)
admin.site.register(HypeSnapshot)
admin.site.register(DemandSnapshot)
admin.site.register(ScrapeLog)