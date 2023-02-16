"""Views for tag app"""

from datetime import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from console_api.config.logger_config import logger
from console_api.tag.models import Tag, IndicatorTagRelationship
from console_api.tag.services import get_new_tag_id, calculate_tags_weight
from console_api.services import create_audit_log_entry, get_not_fields_error
from console_api.tag.serializers import TagCreateSerializer, TagsListSerializer
from console_api.services import (
    CustomTokenAuthentication,
    get_response_with_pagination,
    get_sort_by_param,
)
from console_api.tag.constants import LOG_SERVICE_NAME


class TagsView(APIView):
    """Create a new tag or return list of tags"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Tag.objects.filter(deleted_at=None)

    __SORT_BY_PARAMS = (
        "title", "-title", "weight", "-weight", "created_at", "-created_at",
        "updated_at", "-updated_at",
    )

    def __create_post_log_entry(self, request: Request, tag_data: dict) -> None:
        """Create a log entry for POST method"""

        create_audit_log_entry(request, {
            "table": LOG_SERVICE_NAME,
            "event_type": "create-tag",
            "object_type": "tag",
            "object_name": "Tag",
            "description": "Create a new tag",
            "new_value": tag_data,
        })

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Create a new tag"""

        if error_400 := get_not_fields_error(request, ("title", "weight")):
            return error_400

        tag_data = {
            "id": get_new_tag_id(),
            "title": request.data.get("title"),
            "weight": request.data.get("weight"),
        }
        tag = TagCreateSerializer(data=tag_data)

        if tag.is_valid():
            tag.save()

            self.__create_post_log_entry(request, tag_data)

            return Response(status=HTTP_201_CREATED)
        elif Tag.objects.filter(title=tag_data["title"]):
            tag = Tag.objects.get(title=tag_data["title"])
            tag.deleted_at = None
            tag.save()

            self.__create_post_log_entry(request, tag_data)

            return Response(status=HTTP_201_CREATED)

        return Response(tag.errors, status=HTTP_400_BAD_REQUEST)

    def get(self, request: Request, *args, **kwargs) -> Response:
        """Return a list of tags"""

        sort_by = get_sort_by_param(request)

        if sort_by and sort_by in self.__SORT_BY_PARAMS:
            self.queryset = self.queryset.order_by(sort_by)

        return get_response_with_pagination(
            request, self.queryset, TagsListSerializer
        )


class DeleteOrUpdateTagView(APIView):
    """Delete the tag"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """Mark the tag as deleted"""
        now = datetime.now()
        tag_id = kwargs.get("tag_id")

        if not Tag.objects.filter(id=tag_id, deleted_at=None).exists():
            return Response(
                {"detail": "Tag doesn't exists"},
                status=HTTP_400_BAD_REQUEST
            )

        tag = Tag.objects.get(id=tag_id)
        prev_tag_value = {
            "id": tag.id,
            "title": tag.title,
            "weight": str(tag.weight),
            "created_by": tag.created_by,
            "created_at": str(tag.created_at) if tag.created_at else tag.created_at,
            "updated_at": str(tag.updated_at) if tag.updated_at else tag.updated_at,
            "deleted_at": str(tag.deleted_at) if tag.deleted_at else tag.deleted_at,
        }

        tag.deleted_at = now
        tag.save()

        create_audit_log_entry(request, {
            "table": LOG_SERVICE_NAME,
            "event_type": "delete-tag",
            "object_type": "tag",
            "object_name": "Tag",
            "description": "Delete a tag",
            "prev_value": prev_tag_value,
            "new_value": {
                "id": tag.id,
                "title": tag.title,
                "weight": str(tag.weight),
                "created_by": tag.created_by,
                "created_at": str(tag.created_at) if tag.created_at else tag.created_at,
                "updated_at": str(tag.updated_at) if tag.updated_at else tag.updated_at,
                "deleted_at": str(tag.deleted_at) if tag.deleted_at else tag.deleted_at,
            },
        })
        self.delete_tag_indicator_relationship(deleted_at=now, tag_id=tag_id, request=request)
        self.recalculate_indicator_tags_weight(tag_id=tag_id, updated_at=now, request=request)
        return Response(status=HTTP_200_OK)

    @staticmethod
    def recalculate_indicator_tags_weight(tag_id: int, updated_at: datetime, request: Request):
        calculate_tags_weight(tag_id=tag_id, updated_at=updated_at, request=request)
        logger.info("Indicator tags_weight recalculated")

    @staticmethod
    def delete_tag_indicator_relationship(deleted_at: datetime, tag_id: int, request: Request):
        IndicatorTagRelationship.objects.filter(
            tag_id=tag_id
        ).update(
            deleted_at=deleted_at,
            deleted_by=request.user.id,
            is_deleted=True
        )
        logger.info("Indicator tag relationship deleted")

    def post(self, request: Request, *args, **kwargs) -> Response:
        tag_id = kwargs.get("tag_id")

        if not Tag.objects.filter(id=tag_id).exists():
            return Response(
                {"detail": f"Indicator with id {tag_id} doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        tag = Tag.objects.get(id=tag_id)

        prev_tag_value = {
            "id": tag.id,
            "title": tag.title,
            "weight": str(tag.weight),
            "created_by": tag.created_by,
            "created_at": str(tag.created_at) if tag.created_at else tag.created_at,
            "updated_at": str(tag.updated_at) if tag.updated_at else tag.updated_at,
            "deleted_at": str(tag.deleted_at) if tag.deleted_at else tag.deleted_at,
        }

        if title := request.data.get("title"):
            tag.title = title

        if weight := request.data.get("weight"):
            tag.weight = weight

        tag.save()

        create_audit_log_entry(request, {
            "table": LOG_SERVICE_NAME,
            "event_type": "update-tag",
            "object_type": "tag",
            "object_name": "Tag",
            "description": f"Update tag with id {tag_id}",
            "prev_value": prev_tag_value,
            "new_value": {
                "id": tag.id,
                "title": tag.title,
                "weight": str(tag.weight),
                "created_by": tag.created_by,
                "created_at": str(tag.created_at) if tag.created_at else tag.created_at,
                "updated_at": str(tag.updated_at) if tag.updated_at else tag.updated_at,
                "deleted_at": str(tag.deleted_at) if tag.deleted_at else tag.deleted_at,
            },
        })

        return Response(status=status.HTTP_200_OK)
