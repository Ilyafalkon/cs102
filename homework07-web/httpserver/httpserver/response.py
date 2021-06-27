import dataclasses
import http
import typing as tp


@dataclasses.dataclass
class HTTPResponse:
    status: int
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)
    body: bytes = b""

    def to_http1(self) -> bytes:
        response_status = http.HTTPStatus(self.status)
        value = str(response_status.value).encode()
        phrase = response_status.phrase.encode()

        status_line = b"HTTP/1.1" + b" " + value + b" " + phrase
        headers_line = "\r\n".join(
            [f"{key}: {value}" for key, value in self.headers.items()]
        ).encode()

        return status_line + b"\r\n" + headers_line + b"\r\n\r\n" + self.body
