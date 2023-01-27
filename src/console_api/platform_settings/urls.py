"""Urls for search app"""

from django.urls import path

from console_api.platform_settings.views import PlatformSettingsView


urlpatterns = [
    path(
        "/<key>",
        PlatformSettingsView.as_view(),
        name="platform-settings",
    ),
]
