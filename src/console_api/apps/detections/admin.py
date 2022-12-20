"""Admin interface for detections app"""

from django.contrib import admin

from apps.detections.models import Detection


admin.site.register(Detection)
