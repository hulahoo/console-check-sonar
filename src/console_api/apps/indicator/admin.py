from django.contrib import admin

from apps.indicator.models import Indicator, IndicatorActivities, Session


admin.site.register(Indicator)
admin.site.register(IndicatorActivities)
admin.site.register(Session)
