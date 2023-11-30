from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from wokengineers.helpers.custom_helpers import get_response, CustomExceptionHandler
from wokengineers.status_code import success, object_not_found
from wokengineers.consts import STATUS_INACTIVE

class CustomCreateModelMixin:
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise CustomExceptionHandler(serializer.errors)
        self.perform_create(serializer)
        response = get_response(success, serializer.data)
        headers = self.get_success_headers(response)
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class CustomListModelMixin:
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        response = get_response(success, serializer.data)
        return Response(response)


class CustomRetrieveModelMixin:
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = get_response(success, serializer.data)
        return Response(response)


class CustomUpdateModelMixin:
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            raise CustomExceptionHandler(serializer.errors)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        response = get_response(success, serializer.data)
        return Response(response)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class CustomDestroyModelMixin:
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        
        try:
            obj = self.get_object()
        except Http404:
            raise CustomExceptionHandler(object_not_found)
            
        self.perform_destroy(instance)
        response = get_response(success)
        return Response(response)

    def perform_destroy(self, instance):
        instance.status = STATUS_INACTIVE
        instance.save()
