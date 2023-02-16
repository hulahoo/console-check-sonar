"""Views for files app"""
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_406_NOT_ACCEPTABLE, HTTP_201_CREATED
from rest_framework.parsers import MultiPartParser, FormParser

from console_api.files.forms import UploadFileForm
from console_api.files.models import Files
from console_api.files.services import update_key_with_ts, get_hash
from console_api.services import (
    CustomTokenAuthentication,
)


class FilesView(APIView):
    # authentication_classes = [CustomTokenAuthentication]
    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request: Request, *args, **kwargs) -> Response:
        key = kwargs.get("key")
        bucket = kwargs.get("bucket")

        instance = Files.objects.get(key=key, bucket=bucket)

        file_content = instance.content

        response = HttpResponse(file_content, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="' + key + '"'
        return response

    def post(self, request: Request, *args, **kwargs) -> Response:
        key = kwargs.get("key")
        bucket = kwargs.get("bucket")

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            content = request.FILES['file'].read()
            hash_md5, hash_sha1, hash_sha256 = get_hash(content)
            key = update_key_with_ts(key + '_' + request.FILES['file'].name)
            instance = Files(
                content=content,
                key=key,
                bucket=bucket,
                hash_md5=hash_md5,
                hash_sha1=hash_sha1,
                hash_sha256=hash_sha256),
            instance.save()

            return Response(status=HTTP_201_CREATED,
                            data={'file-size': request.FILES['file'].size,
                                  'file-name': key,
                                  'hash-md5': hash_md5,
                                  'hash-sha1': hash_sha1,
                                  'hash-sha256': hash_sha256}
                            )
        else:
            return Response(status=HTTP_406_NOT_ACCEPTABLE)
