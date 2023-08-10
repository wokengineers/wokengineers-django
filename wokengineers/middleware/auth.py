
from wokengineers.consts import *
import jwt


import threading

request_local = threading.local()


def get_request():
    return getattr(request_local, 'request', None)


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #  After request the code will go here
        authorization = request.headers.get("Authorization")
        token = authorization.split(" ")[1] if authorization else authorization
        request.token = token
        if token:
            decoded = jwt.decode(token, options={"verify_signature": False})
            auth_id = decoded.get("auth_id")
            user_name = decoded.get("name")
            role = decoded.get("roles",[None])[0]
            request.auth_id = auth_id
            request.user_name = user_name
            request.role = role
        else:
            request.auth_id = CREATION_BY
            request.user_name = CREATION_BY
            request.role = DEFAULT_ROLE

        request_local.request = request
        response = self.get_response(request)

        # After response code will go here

        return response
