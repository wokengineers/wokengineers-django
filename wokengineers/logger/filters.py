import logging
from wokengineers.middleware.auth import get_request
from wokengineers.logger.consts import FILTER_DEFAULT_DICT


class CustomLoggerFilter(logging.Filter):
    def __init__(self, filter_dict=None):
        if filter_dict:
            self.filter_dict = filter_dict
        else:
            self.filter_dict = {}
        self.filter_dict.update(FILTER_DEFAULT_DICT)
        for key in self.filter_dict:
            setattr(self, key, self.filter_dict[key])

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def filter(self, record):
        try:
            record.ip = self.get_client_ip(get_request())
        except:
            record.ip = ""
        
        for key, value in self.filter_dict.items():
            try:
                values = value.split(",")
                attr = values[0]
                value = getattr(get_request(), attr)
                if len(values) == 2:
                    attr, val = values[0], values[1]
                    value = value[val]
            except Exception as e:
                value = ""

            setattr(record, key, value)

        return True
