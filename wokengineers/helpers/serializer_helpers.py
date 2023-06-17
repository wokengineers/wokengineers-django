import logging
from wokengineers.consts import STATUS_ACTIVE, CREATION_BY
from wokengineers.middleware.auth import get_request
import datetime
from wokengineers.serializers import CustomCharField, CustomIntegerField, serializers

logger = logging.getLogger("django")


def common_add_required_data_in_json(field, is_create=True):
    request = get_request()
    if is_create:
        field['creation_date'] = datetime.datetime.now()
        field['status'] = STATUS_ACTIVE
        if request:
            field['creation_by'] = request.user_id
        else:
            field['creation_by'] = CREATION_BY
        
    else:
        field["updation_date"] = datetime.datetime.now()
        if request:
            field["updation_by"] = request.user_id
        else:
            field["updation_by"] = CREATION_BY

    return field


def help_text_for_dict(dict_value):
    """_summary_

    Args:
        dict_value (_type_): Dict type

    Returns:
        _type_: String Format help text
    """
    return f'Enter value from this list - {list(dict_value.keys())}'


class SuccessResponseSerializer(serializers.Serializer):
    status = CustomIntegerField(required=True)
    message = CustomCharField(required=True)