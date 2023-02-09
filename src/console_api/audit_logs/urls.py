"""Urls for audit_logs app"""

from django.urls import path

from console_api.audit_logs.views import AuditLogsFiltersView, AuditLogsListView


urlpatterns = [
    path("", AuditLogsListView.as_view(), name="audit_logs"),
    path("/filters", AuditLogsFiltersView.as_view(), name="audit_logs_filters"),
]
