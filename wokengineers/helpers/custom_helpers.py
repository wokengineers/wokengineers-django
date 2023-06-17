import logging
from wokengineers.status_code import field_should_be_int_type
from datetime import datetime
from wokengineers.consts import DATE_YYYY_MM_DD
import re 

logger = logging.getLogger("django")


class CustomExceptionHandler(Exception):
    def __init__(self, detail='', status_code=400):
        # Call the base class constructor with the parameters it needs
        super(CustomExceptionHandler, self).__init__(detail)
        self.status_code = status_code
        self.detail = detail
    
def log_info_message(request, message = "Info"):
    return (f"{message} --> {request.body}")

def get_response(status_attribute, data=None):
    if data is None:
        return {'status': status_attribute['status_code'], 'message': status_attribute['message']}
    else:
        return {'status': status_attribute['status_code'], 'message': status_attribute['message'], 'data': data}


def validate_value_regex(value, error_label, validation_type, regex=None): 
    if validation_type == "mob":
        regex = r'^[123456789]\d{9}$'
    elif validation_type == "email":
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    if value is not None:
        if re.fullmatch(regex, value):
            return True
        else:
            logger.exception("exception : %s",error_label)
            raise CustomExceptionHandler(error_label)
    return value



def int_float_check(label, data):
    if isinstance(data, str) and (data.strip().isdigit() or str(data).replace('.', '', 1).isdigit()):
        data = int(data) if data.strip().isdigit() else float(data)
    elif not isinstance(data, (int, float)):
        logger.exception("exception : %s", field_should_be_int_type(label))
        raise CustomExceptionHandler(field_should_be_int_type(label))
    return data




def common_checking_and_passing_value_from_list_dict(value, list_dict, error_label):
    """
    merged two functions common_dict_checking_and_passing_value, common_list_checking
    """
    if value == "":
        return None
    
    if value:
        if type(list_dict) == list:
            if value not in list_dict:
                logger.exception("exception : %s",error_label)
                raise CustomExceptionHandler(error_label)
            return value
        else:
            if value not in list_dict.keys():
                logger.exception("exception : %s",error_label)
                raise CustomExceptionHandler(error_label)
            return list_dict[value]
    return value



def common_date_format_check_passing_value(value, date_format, error_label):
    if value:
        try:
            return datetime.strptime(value, date_format).date()
        except:
            logger.exception("exception : %s", error_label)
            raise CustomExceptionHandler(error_label)
    return value



def dict_get_key_from_value(dict_obj, dict_val):
    if dict_val is not None:
        key_list = list(dict_obj.keys())
        val_list = list(dict_obj.values())
        try:
            position = val_list.index(int(dict_val))
        except:
            position = val_list.index(dict_val)
        return key_list[position]
    else: 
        return None 



