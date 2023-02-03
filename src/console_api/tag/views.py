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

from console_api.tag.models import Tag
from console_api.tag.services import get_new_tag_id
from console_api.services import create_audit_log_entry, get_not_fields_error
from console_api.tag.serializers import TagCreateSerializer, TagsListSerializer
from console_api.services import (
    CustomTokenAuthentication,
    get_response_with_pagination,
)
from console_api.tag.constants import LOG_SERVICE_NAME


class TagsView(APIView):
    """Create a new tag or return list of tags"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

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

        return get_response_with_pagination(
            request=request,
            objects=Tag.objects.filter(deleted_at=None),
            serializer=TagsListSerializer,
        )


class DeleteTagView(APIView):
    """Delete the tag"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """Mark the tag as deleted"""

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

        tag.deleted_at = datetime.now()
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

        return Response(status=HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs) -> Response:
        tag_id = kwargs.get("tag_id")
        title = request.data.get("title")

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

        tag.title = title
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

        return Response(TagCreateSerializer(instance=tag).data, status=status.HTTP_200_OK)
