from typing import Optional
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.views import exception_handler


# Success Response Utility
def success_response(data: dict = None, message: str = "Operation successful", status_code: int = status.HTTP_200_OK):
    return Response(
        {
            "success": True,
            "message": message,
            "data": data or None,
        },
        status=status_code
    )


# Failure Response Utility
def failure_response(message: str, status_code: int, errors: Optional[dict] = None):
    return Response(
        {
            "success": False,
            "message": message,
            "data": errors or None,
        },
        status=status_code
    )


# Middleware for Exception Handling
class ExceptionHandlingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        # Handle ValidationError
        if isinstance(exception, ValidationError):
            return failure_response(
                message="Validation error",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                errors=exception.message_dict
            )

        # Handle NotFound
        elif isinstance(exception, Http404) or isinstance(exception, NotFound):
            return failure_response(
                message="Resource not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )   

        # Handle APIException
        elif isinstance(exception, APIException):
            return failure_response(
                message="API error",
                status_code=exception.status_code,
                errors=exception.detail
            )

        # Handle ValueError
        elif isinstance(exception, ValueError):
            return failure_response(
                message=str(exception),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Handle other exceptions
        else:
            return failure_response(
                message="Internal server error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
       


