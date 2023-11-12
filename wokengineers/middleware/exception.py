from wokengineers.helpers.custom_helpers import CustomExceptionHandler, get_response
from django.http import JsonResponse
import traceback
import logging
from wokengineers.status_code import generic_error_2

logger = logging.getLogger("django")

class CustomExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        if exception:
            message = "**{url}**\n\n{error}\n\n````{tb}````".format(
                    url=request.build_absolute_uri(),
                    error=repr(exception),
                    tb=traceback.format_exc()
                )

        message = ""

        if isinstance(exception, CustomExceptionHandler):
            logger.exception(f"CustomException {message}")
            response_obj = get_response(eval(str(exception)))
            status_code = 400
        else:
            logger.exception(f"Exception {message}")
            response_obj = get_response(generic_error_2)
            status_code = 500

        return JsonResponse(response_obj, status=status_code)