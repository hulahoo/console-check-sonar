"""Views for tag app"""

from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from console_api.services import (
    CustomTokenAuthentication,
    get_response_with_pagination,
)
from console_api.tag.models import Tag
from console_api.tag.serializers import TagCreateSerializer, TagsListSerializer
from console_api.tag.services import get_new_tag_id


class TagsView(APIView):
    authentication_classes = [CustomTokenAuthentication]

    def post(self, request: Request, *args, **kwargs) -> Response:
        for field in "title", "weight":
            if not request.data.get(field):
                return Response(
                    {"detail": f"{field} not specified"},
                    status=HTTP_400_BAD_REQUEST,
                )

        tag_data = {
            "id": get_new_tag_id(),
            "title": request.data.get("title"),
            "weight": request.data.get("weight"),
        }
        tag = TagCreateSerializer(data=tag_data)

        if tag.is_valid():
            tag.save()

            return Response(status=HTTP_201_CREATED)

    def get(self, request: Request, *args, **kwargs) -> Response:
        return get_response_with_pagination(
            request=request,
            objects=Tag.objects.filter(deleted_at=None),
            serializer=TagsListSerializer,
        )


class DeleteTag(APIView):
    authentication_classes = [CustomTokenAuthentication]

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """Mark the tag as deleted"""
        tag_id = kwargs.get("tag_id")
        if not Tag.objects.filter(id=tag_id).exists():
            return Response(
                {"detail": "Token doesn't exists"},
                status=HTTP_400_BAD_REQUEST
            )

        tag = Tag.objects.get(id=tag_id)
        tag.deleted_at = datetime.now()
        tag.save()

        return Response(status=HTTP_200_OK)
