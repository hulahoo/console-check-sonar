"""Views for the project"""

from django.http import JsonResponse


def custom_404_handler(exception=None) -> JsonResponse:
    """Custom handler for 404 error"""

    return JsonResponse({
        'error': f'The resource was not found: {exception}'
    }, status=404)
