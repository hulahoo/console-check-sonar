"""Views for the project"""

from django.http import JsonResponse


def custom_404_handler(request, exception=None) -> JsonResponse:
    """Custom handler for 404 error"""

    return JsonResponse({
        'error': 'The resource was not found'
    }, status=404)
