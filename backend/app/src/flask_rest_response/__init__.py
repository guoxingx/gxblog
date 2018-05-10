
"""
*** Example
***

from flask_rest_response import Error, Collection, response


class SmsCodeErrors(Collection):
    code = '100'
    errmsg = 'sms code: '

    sms_code_request_too_often = Error('01', 'request too often.')
    sms_code_request_forbidden = Error('02', 'request forbidden today.')


@SmsCodeErrors()
class Api(object):

    @response()
    def get(self):

        # error
        return self.get_error('01')
        return self.get_error('sms_code_request_forbidden')

        # success
        return {'user_id': 123}

***end of Example
***
"""

from .response import response, json_required
from .errors import Error, Collection, get_error
from .utils import init_config
