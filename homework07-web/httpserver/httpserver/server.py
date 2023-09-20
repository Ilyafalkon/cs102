import socket
import threading
import time
import typing as tp

from .handlers import BaseHTTPRequestHandler, BaseRequestHandler


class TCPServer:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5000,
        backlog_size: int = 1,
        max_workers: int = 1,
        timeout: tp.Optional[float] = None,
        request_handler_cls: tp.Type[BaseRequestHandler] = BaseRequestHandler,
    ) -> None:
        self.host = host
        self.port = port
        self.server_address = (host, port)
        self.backlog_size = backlog_size
        self.request_handler_cls = request_handler_cls
        self.max_workers = max_workers
        self.timeout = timeout
        self._shutdown_event = threading.Event()
        self._threads: tp.List[threading.Thread] = []
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def serve_forever(self) -> None:
        """Called to start the server"""
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self._server_socket.bind(self.server_address)
        print(f"Server running at http://{self.host}:{self.port}\n")
        self._server_socket.listen(self.backlog_size)
        for _ in range(self.max_workers):
            t = threading.Thread(target=self.worker_thread, daemon=True)
            t.start()
            self._threads.append(t)
        try:
            for t in self._threads:
                t.join()
        except KeyboardInterrupt:
            print(f"\nServer {self.host}:{self.port} shutting down")
        finally:
            self._server_socket.close()
            self._shutdown_event.set()
            time.sleep(1)

    def handle_accept(
        self, client_socket: socket.socket, client_address: tp.Tuple[str, int]
    ) -> None:
        """Called to process client request"""
        if self.timeout:
            client_socket.settimeout(self.timeout)
        handler = self.request_handler_cls(
            socket=client_socket, address=client_address, server=self
        )
        handler.handle()

    def worker_thread(self) -> None:
        """Executes instructions while threads are on"""
        while not self._shutdown_event.is_set():
            try:
                client_socket, client_address = self._server_socket.accept()
                print(f"New client: {client_address[0]}:{client_address[1]}")

                self.handle_accept(client_socket, client_address)
            except ConnectionAbortedError:
                break


class HTTPServer(TCPServer):
    pass
