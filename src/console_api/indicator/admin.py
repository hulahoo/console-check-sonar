"""Admin panel for indicator app"""

from django.contrib import admin

from console_api.indicator.models import (
    Indicator,
    IndicatorActivities,
    Session,
)


admin.site.register(Indicator)
admin.site.register(IndicatorActivities)
admin.site.register(Session)
