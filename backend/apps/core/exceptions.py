from rest_framework.views import exception_handler

def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    request = context.get("request")
    request_id = getattr(request, "request_id", None)

    response.data = {
        "error": {
            "status_code": response.status_code,
            "details": response.data,
            "request_id": request_id,
        }
    }
    return response
