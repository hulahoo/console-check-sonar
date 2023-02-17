"""Urls for search app"""

from django.urls import path

from console_api.search.views import (
    search_indicators_view,
    search_detections_by_text_view,
    search_history_view,
    SearchTagsView, file_search_job_status, file_search_job_result, file_search_start_job,
    file_search_stop_job,
)

urlpatterns = [
    path(
        "/history",
        search_history_view,
        name="history",
    ),
    path(
        "/indicators",
        search_indicators_view,
        name="by_text",
    ),
    path(
        "/detections/by-text",
        search_detections_by_text_view,
        name="detections_by_text",
    ),
    path(
        "/tags/by-title",
        SearchTagsView.as_view(),
        name="tags_by_title"
    ),
    path(
        "/from-file/status",
        file_search_job_status,
        name="search_from_file_log_txt_job_status"
    ),
    path(
        "/from-file/result",
        file_search_job_result,
        name="search_from_file_log_txt_job_result"
    ),
    path(
        "/from-file/start-job",
        file_search_start_job,
        name="search_from_file_log_txt_start_job"
    ),
    path(
        "/from-file/stop-job",
        file_search_stop_job,
        name="search_from_file_log_txt_start_job"
    )
]
