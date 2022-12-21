from django.contrib import admin

from apps.indicator.models import Indicator

from apps.indicator.models import IndicatorActivities

admin.site.register(Indicator)
admin.site.register(IndicatorActivities)
