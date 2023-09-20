import typing as tp

from httpserver import BaseHTTPRequestHandler, HTTPServer

from .request import WSGIRequest
from .response import WSGIResponse


class WSGIServer(HTTPServer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app: tp.Optional[tp.Any] = None

    def set_app(self, app: tp.Any) -> None:
        self.app = app

    def get_app(self) -> tp.Optional[tp.Any]:
        return self.app


class WSGIRequestHandler(BaseHTTPRequestHandler):
    request_klass = WSGIRequest
    response_klass = WSGIResponse

    def handle_request(self, request: WSGIRequest) -> WSGIResponse:
        environ = request.to_environ()
        environ["WSGIserver.socket"] = self.server._server_socket
        environ["SERVER_NAME"], environ["SERVER_PORT"] = self.server.server_address
        app = self.server.get_app()
        response = self.response_klass()
        result = app(environ, response.start_response)
        for data in result:
            response.body += data
        return response
