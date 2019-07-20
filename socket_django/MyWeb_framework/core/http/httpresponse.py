class Http2xxResponse:
    status_code = 200
    status_content = "OK"


class Http3xxResponse:
    status_code = 302
    status_content = 'Found'


class Http404Response:
    status_code = 404
    status_content = 'Not Found'


class Http5xxResponse:
    status_code = 500
    status_content = 'Error'
