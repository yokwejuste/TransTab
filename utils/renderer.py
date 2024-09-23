from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler
from django.utils import timezone
import uuid


class NewJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code

        if 200 <= status_code < 300:
            response = {"status": "success", "statusCode": status_code, "data": data}
        else:
            response = {
                "status": "error",
                "statusCode": status_code,
                "error": {
                    "code": data.get("code", "UNKNOWN_ERROR"),
                    "message": data.get("detail", str(data)),
                    "details": data.get("details", None),
                    "timestamp": timezone.now().isoformat(),
                    "path": renderer_context["request"].path,
                    "suggestion": data.get("suggestion", None),
                },
            }

        response["requestId"] = str(uuid.uuid4())
        response["documentation_url"] = "https://api.example.com/docs/errors"

        return super().render(response, accepted_media_type, renderer_context)


def trans_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data["status"] = "error"
        response.data["statusCode"] = response.status_code

    return response
