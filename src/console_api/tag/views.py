"""Views for tag app"""

from django.views.decorators.http import (
    require_http_methods,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)

from console_api.services import (
    CustomTokenAuthentication,
    get_response_with_pagination,
)
from console_api.constants import CREDS_ERROR
from console_api.tag.models import Tag
from console_api.tag.serializers import TagCreateSerializer, TagsListSerializer


@api_view(["POST", "GET"])
@require_http_methods(["GET", "POST"])
def tags_view(request: Request) -> Response:
    """View for /tags endpoint"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response({"detail": CREDS_ERROR}, status=HTTP_403_FORBIDDEN)

    if request.method == "POST":
        for field in "title", "weight":
            if not request.data.get(field):
                return Response(
                    {"detail": f"{field} not specified"},
                    status=HTTP_400_BAD_REQUEST,
                )

        tag_data = {
            "id": Tag.objects.order_by("id").last().id + 1,
            "title": request.data.get("title"),
            "weight": request.data.get("weight"),
        }
        tag = TagCreateSerializer(data=tag_data)

        if tag.is_valid():
            tag.save()

            return Response(status=HTTP_201_CREATED)

        return Response(tag.errors, status=HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        return get_response_with_pagination(
            request=request,
            objects=Tag.objects.all(),
            serializer=TagsListSerializer,
        )

    return Response(status=HTTP_400_BAD_REQUEST)
