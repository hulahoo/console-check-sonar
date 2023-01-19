from django.views.decorators.http import require_safe, require_POST, require_http_methods # noqa

require_GET_DELETE = require_http_methods(["DELETE,  GET"])
require_GET_DELETE.__doc__ = "Decorator to require that a view accept the DELETE and GET method."

require_PATCH = require_http_methods(["PATCH"])
require_PATCH.__doc__ = "Decorator to require that a view only accepts the PATCH method."

require_GET_POST = require_http_methods(["GET", "POST"])
require_GET_POST.__doc__ = "Decorator to require that a view accept the POST and GET method."

require_POST_DELETE = require_http_methods(["POST", "DELETE"])
require_POST_DELETE.__doc__ = "Decorator to require that a view accept the POST and DELETE method."
