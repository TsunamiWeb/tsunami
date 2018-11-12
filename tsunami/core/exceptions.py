from tsunami.core import response as _resp


class APIException(Exception):

    code = _resp.CODE_1_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = detail
        else:
            self.detail = self.default_detail

    def __str__(self):
        return self.detail
