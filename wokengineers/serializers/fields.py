from rest_framework import serializers
from rest_framework.fields import empty
import logging
from kuantam.status_code import field_cannot_be_blank, field_list_cannot_be_empty, field_required_error, field_should_be_boolean_type, \
    field_should_be_int_type, field_should_be_list_type, field_should_be_string_type, table_not_exist
from kuantam.consts import STATUS_ACTIVE
from kuantam.helpers.custom_helpers import CustomExceptionHandler, int_float_check

logger = logging.getLogger("django")


class IsActiveListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(status=STATUS_ACTIVE)
        return super().to_representation(data)


class CustomIntegerField(serializers.IntegerField):
    def __init__(self, **kwargs):
        self.restrict_roles = kwargs.pop('restrict_roles', [])

        super().__init__(**kwargs)
        self.allow_null = kwargs.pop('allow_null', True)

    def run_validation(self, data=empty):
        # Test for the empty string here so that it does not get validated,
        # and so that subclasses do not need to handle it explicitly
        # inside the `to_internal_value()` method.

        if not self.required and data in [empty, "", None]:
            return None

        if not getattr(self.root, "partial", False):
            if self.required and data in [empty, "", None]:
                # Handle field if required is True but field is not pass
                # Self.required is pass because field can be required in model file
                logger.exception("Exception : %s",field_required_error(self.label))
                raise CustomExceptionHandler(field_required_error(self.label))

        if not getattr(self.root, "partial", False):
            data = int_float_check(self.label, data)

        elif data is not empty:
            data = int_float_check(self.label, data)

        return super().run_validation(data)

    def to_internal_value(self, value):
        return value


class CustomCharField(serializers.CharField,):
    def __init__(self, **kwargs):
        self.restrict_roles = kwargs.pop('restrict_roles', [])
        self.store_lower = kwargs.pop('store_lower', True)
        super().__init__(**kwargs)

        self.allow_blank = kwargs.pop('allow_blank', True)
        self.allow_null = kwargs.pop('allow_null', True)

    def run_validation(self, data=empty):
        # Test for the empty string here so that it does not get validated,
        # and so that subclasses do not need to handle it explicitly
        # inside the `to_internal_value()` method.

        if not self.required and data in [empty, "", None]:
            return None

        if not getattr(self.root, "partial", False):
            if self.required and data in [empty, "", None]:
                # Handle field if required is True but field is not pass
                # Self.required is pass because field can be required in model file
                logger.exception("Exception : %s",field_required_error(self.label))
                raise CustomExceptionHandler(field_required_error(self.label))

            if data == "" and not self.allow_blank:
                # Handle field if required is True but field is not passed
                logger.exception("Exception : %s",field_cannot_be_blank(self.label))
                raise CustomExceptionHandler(field_cannot_be_blank(self.label))

            if not isinstance(data, str):
                logger.exception("Exception : %s",field_should_be_string_type(self.label))
                raise CustomExceptionHandler(
                    field_should_be_string_type(self.label))
            else:
                data = data.strip().lower() if self.store_lower else data.strip()

        if data != empty and isinstance(data, str):
            data = data.strip().lower() if self.store_lower else data.strip()
        return super().run_validation(data)


class CustomListField(serializers.ListField):
    def __init__(self, **kwargs):
        self.restrict_roles = kwargs.pop('restrict_roles', [])

        super().__init__(**kwargs)
        self.allow_null = kwargs.pop('allow_null', True)

    def run_validation(self, data=empty):
        # Test for the empty string here so that it does not get validated,
        # and so that subclasses do not need to handle it explicitly
        # inside the `to_internal_value()` method.

        if not self.required and data in [empty, "", None]:
            return None

        if not getattr(self.root, "partial", False):
            if self.required and data in [empty, "", None]:
                # Handle field if required is True but field is not pass
                # Self.required is pass because field can be required in model file
                logger.exception("Exception : %s",
                                 field_required_error(self.label))
                raise CustomExceptionHandler(field_required_error(self.label))

        if not getattr(self.root, "partial", False):
            if not isinstance(data, list):
                logger.exception("Exception : %s",
                                 field_required_error(self.label))
                raise CustomExceptionHandler(
                    field_should_be_list_type(self.label))

            if len(data) == 0:
                logger.exception("Exception : %s",
                                 field_list_cannot_be_empty(self.label))
                raise CustomExceptionHandler(
                    field_list_cannot_be_empty(self.label))

        if len(data) != 0 and isinstance(data, list):
            data = data

        # elif data is not empty:
        #     data = data.strip().lower()

        return super().run_validation(data)


class CustomBooleanField(serializers.BooleanField):
    def __init__(self,  **kwargs):
        self.default_value = kwargs.pop('default',None)
        self.restrict_roles = kwargs.pop('restrict_roles', [])

        super().__init__(**kwargs)
        self.allow_null = kwargs.pop('allow_null', True)

    def run_validation(self, data=empty):
        # Test for the empty string here so that it does not get validated,
        # and so that subclasses do not need to handle it explicitly
        # inside the `to_internal_value()` method.
        # if not self.required and self.default == empty:
        #     return None
        if not self.required and data in [empty, "", None]  :
            return self.default_value 

        if not getattr(self.root, "partial", False):
            if self.required and data in [empty, "", None]:
                # Handle field if required is True but field is not pass
                # Self.required is pass because field can be required in model file
                logger.exception("Exception : %s",field_required_error(self.label))
                raise CustomExceptionHandler(field_required_error(self.label))

        if not getattr(self.root, "partial", False):
            if not isinstance(data, bool):
                logger.exception("Exception : %s",field_should_be_boolean_type(self.label))
                raise CustomExceptionHandler(field_should_be_boolean_type(self.label))

        return super().run_validation(data)

    def to_internal_value(self, value):
        return value

    def to_representation(self, value):
        return value


class CustomForeignField(serializers.PrimaryKeyRelatedField):
     def _init_(self, **kwargs):
         self.restrict_roles = kwargs.pop('restrict_roles', [])
         self.model = kwargs.pop('model', [])
         self.field = kwargs.pop('field', [])
         self.lable = kwargs.pop('lable', [])
         self.error= kwargs.pop('error', [])
         self.allow_null = kwargs.pop('allow_null', True)
         super()._init_(**kwargs)
         self.required = kwargs.pop('required', [])
         serializers.PrimaryKeyRelatedField._init_(self,required=self.required)
 
 
     def run_validation(self, data=empty):
         # Test for the empty string here so that it does not get validated,
         # and so that subclasses do not need to handle it explicitly
         # inside the `to_internal_value()` method.
 
         if not self.required and data in [empty, "", None]:
             return None
 
         if not getattr(self.root, "partial", False):
             if self.required and data in [empty, "", None]:
                 # Handle field if required is True but field is not pass
                 # Self.required is pass because field can be required in model file
                 # logger.exception("Exception : %s",
                 #                  field_required_error(self.label))
                 raise CustomExceptionHandler(field_required_error(self.label))
 
         if not getattr(self.root, "partial", False):
             if (not isinstance(data, int)) and (not data.strip().isdigit()):
                 # logger.exception("Exception : %s",
                 #                  field_should_be_int_type(self.label))
                 raise CustomExceptionHandler(
                     field_should_be_int_type(self.label))
 
         return super().run_validation(data)
 
     def get_queryset(self):
         field = self.root._dict_['_kwargs']["data"].get(self.field)
         obj = self.model.objects.filter(id=field,status = STATUS_ACTIVE)
         if not obj.exists():raise CustomExceptionHandler(self.error)
         return obj
 
     def to_representation(self, value):
         return str(value)
