"""Urls for audit_logs app"""

from django.urls import path

from console_api.audit_logs.views import AuditLogsListView


urlpatterns = [
    path("", AuditLogsListView.as_view(), name="audit_logs"),
]
