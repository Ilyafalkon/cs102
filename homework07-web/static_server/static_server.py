import dataclasses
import datetime
import mimetypes
import pathlib
from urllib.parse import unquote, urlsplit

from httpserver import BaseHTTPRequestHandler, HTTPRequest, HTTPResponse, HTTPServer


def url_normalize(url: str) -> str:
    _, _, path, _, _ = urlsplit(url.strip())
    path = unquote(url)
    output, part = [], None  # type:ignore
    for part in path.split("/"):
        if part == "":
            if not output:
                output.append(part)
        elif part == ".":
            pass
        elif part == "..":
            if len(output) > 1:
                output.pop()
        else:
            output.append(part)
    if part in ["", ".", ".."]:
        output.append("")
    path = "/".join(output)

    return path.lower()


class StaticHTTPRequestHandler(BaseHTTPRequestHandler):
    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        srv = "staticserver"
        date = str(datetime.datetime.now())
        allow = "GET, HEAD"

        if request.method != b"GET" and request.method != b"HEAD":
            status = 405
            body = b"405 error"
            headers = {"Server": srv, "Date": date, "Allow": allow}
        elif request.method == b"GET":
            path = url_normalize(request.url.decode())
            path = path[1:] if path[0] == "/" else path
            if not path:
                path = "index.html"

            full_path = server.document_root / path
            if full_path.is_file():
                status = 200
                content_type = mimetypes.guess_type(full_path)[0]
                content_type = "" if not content_type else content_type

                with open(full_path, "rb") as file:
                    body = file.read()

                headers = {
                    "Server": srv,
                    "Date": date,
                    "Content-Length": str(len(body)),
                    "Content-Type": content_type,
                    "Allow": allow,
                }
            else:
                status = 404
                body = b"404 error"
                headers = {"Server": srv, "Date": date}
        else:
            status = 200
            body = b""
            headers = {
                "Server": srv,
                "Date": date,
                "Allow": allow,
            }

        return self.response_klass(status=status, headers=headers, body=body)


class StaticServer(HTTPServer):
    def __init__(self, *args, **kwargs) -> None:
        self.document_root: pathlib.Path = document_root
        del kwargs["document_root"]
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    document_root = pathlib.Path("static") / "root"
    server = StaticServer(
        timeout=5,
        document_root=document_root,
        request_handler_cls=StaticHTTPRequestHandler,
    )
    server.serve_forever()
