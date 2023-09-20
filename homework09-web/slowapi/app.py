import http
import json
import typing as tp
from urllib.parse import parse_qsl

from .request import Request
from .response import JsonResponse, Response
from .router import Route


class SlowAPI:
    def __init__(self):
        self.routes: tp.List[Route] = []
        self.middlewares = []

    def __call__(self, environ, start_response):
        resp_headers = []
        body = [b""]

        is_paths_coincided = False
        response: tp.Optional[tp.Union[Response, JsonResponse]] = None
        path_ = environ["PATH_INFO"]
        if path_[-1] == "/" and path_ != "/":
            path = path_[:-1]
        method = environ["REQUEST_METHOD"]
        query = dict(parse_qsl(environ["QUERY_STRING"]))
        body = environ["wsgi.input"]
        headers = {k[5:]: v for k, v in environ.items() if k.startswith("HTTP_")}
        request = Request(path, method, query, body, headers)

        for route in self.routes:
            all_match, is_path_coincided, params_names, params_values = route.match(
                request.method, request.path
            )

            if all_match:
                if params_names and params_values:
                    response = self.dynamic_path_handler(
                        route.func, request, params_names, params_values
                    )
                else:
                    response = self.static_path_handler(route.func, request)
                break
            if is_path_coincided:
                is_paths_coincided = True

        if response:
            status = response.status
            body_1 = ""
            if isinstance(response, JsonResponse):
                body_1 = json.dumps(response.data, default=response.serializer)
            elif isinstance(response, Response):
                body_1 = str(response.body)
            body = [body_1.encode()]

            if response.content_type:
                resp_headers.append("CONTENT_TYPE", response.content_type)
                resp_headers.append("CONTENT_LENGTH", str(len(body[0])))
            if response.headers:
                resp_headers.append(list(response.headers.items()))
        elif is_paths_coincided:
            status = 405
        else:
            status = 404
        status_phrase = str(http.HTTPStatus(status).value) + " " + http.HTTPStatus(status).phrase
        start_response(status_phrase, resp_headers)
        return body

    def route(self, path=None, method="GET", **options):
        def decorator(func):
            data = []
            methods = []
            if isinstance(path, (tuple, list, set, dict)):
                data = list(path)
            elif path:
                data = [path]
            for particular_path in data or ["/"]:
                if isinstance(method, (tuple, list, set, dict)):
                    methods = list(method)
                elif method:
                    methods = [method]
                for particular_method in methods:
                    particular_method = particular_method.upper()
                    route = Route(particular_path, particular_method, func)
                    self.routes.append(route)
            return func

        return decorator

    def get(self, path=None, **options):
        return self.route(path, method="GET", **options)

    def post(self, path=None, **options):
        return self.route(path, method="POST", **options)

    def patch(self, path=None, **options):
        return self.route(path, method="PATCH", **options)

    def put(self, path=None, **options):
        return self.route(path, method="PUT", **options)

    def delete(self, path=None, **options):
        return self.route(path, method="DELETE", **options)

    def add_middleware(self, middleware) -> None:
        self.middlewares.append(middleware)
