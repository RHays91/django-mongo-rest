import logging
from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django_mongo_rest import ApiException
from django_mongo_rest.utils import json_default_serializer

logger = logging.getLogger('django')

class ApiExceptionMiddleware(MiddlewareMixin):
    @staticmethod
    def process_exception(_, exception):
        if isinstance(exception, ApiException):
            if exception.status_code == 500:
                logger.exception(exception)

            return JsonResponse(exception.__dict__, status=exception.status_code,
                                json_dumps_params={'default': json_default_serializer})
