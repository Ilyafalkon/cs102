from __future__ import annotations

import socket
import typing as tp

from httptools import HttpParserError, HttpRequestParser

from .request import HTTPRequest
from .response import HTTPResponse

if tp.TYPE_CHECKING:
    from .server import TCPServer

Address = tp.Tuple[str, int]


class BaseRequestHandler:
    def __init__(self, socket: socket.socket, address: Address, server: TCPServer) -> None:
        self.socket = socket
        self.address = address
        self.server = server

    def handle(self) -> None:
        self.close()

    def close(self) -> None:
        print(f"Close connection with {self.address[0]}:{self.address[1]}\n")
        self.socket.close()


class EchoRequestHandler(BaseRequestHandler):
    def handle(self) -> None:
        try:
            data = self.socket.recv(1024)
        except (socket.timeout, BlockingIOError):
            pass
        else:
            self.socket.sendall(data)
        finally:
            self.close()


class BaseHTTPRequestHandler(BaseRequestHandler):
    request_klass = HTTPRequest
    response_klass = HTTPResponse

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.parser = HttpRequestParser(self)

        self._url: bytes = b""
        self._headers: tp.Dict[bytes, bytes] = {}
        self._body: bytes = b""
        self._parsed = False

    def handle(self) -> None:
        request = self.parse_request()
        if request:
            try:
                response = self.handle_request(request)
            except Exception:
                # TODO: log exception
                response = self.response_klass(status=500, headers={}, body=b"500 error")
        else:
            response = self.response_klass(status=400, headers={}, body=b"400 error")
        self.handle_response(response)
        self.close()

    def parse_request(self) -> tp.Optional[HTTPRequest]:
        while True:
            try:
                request = self.socket.recv(1024)
            except (socket.timeout, BlockingIOError):
                return None

            try:
                self.parser.feed_data(request)
            except HttpParserError:
                return None

            if self._parsed or not request:
                break

        method = self.parser.get_method()
        return self.request_klass(
            method=method, url=self._url, headers=self._headers, body=self._body
        )

    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        return self.response_klass(status=405, headers={}, body=b"")

    def handle_response(self, response: HTTPResponse) -> None:
        self.socket.sendall(response.to_http1())

    def on_url(self, url: bytes) -> None:
        self._url = url

    def on_header(self, name: bytes, value: bytes) -> None:
        self._headers[name] = value

    def on_body(self, body: bytes) -> None:
        self._body = body

    def on_message_complete(self) -> None:
        self._parsed = True
        print("Message complete")
