import logging
import socketserver
import threading

LOGGER = logging.getLogger(__name__)


class UdpLogServer():
    def __init__(self) -> None:
        self.__server = None
        self.__server_thread = None
        self.__is_shutdown = threading.Event()
        self.__already_shutting_down = False

    class ThreadedRequestHandler(socketserver.BaseRequestHandler):
        """
        This class works similar to the TCP handler class, except that
        self.request consists of a pair of data and client socket, and since
        there is no connection the client address must be given explicitly
        when sending data back via sendto().
        """

        def handle(self):
            data = self.request[0]
            s = self.request[1]
            LOGGER.info(f"Request received for {self.client_address} {data}")

    class ThreadedServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
        def __init__(self, server_address, RequestHandlerClass, is_shutdown):
            self.allow_reuse_address = True
            socketserver.UDPServer.__init__(self, server_address, RequestHandlerClass)
            self.is_shutdown = is_shutdown

    def start(self):
        HOST, PORT = "0.0.0.0", 10000

        try:
            self.__server = self.ThreadedServer((HOST, PORT), self.ThreadedRequestHandler, self.__is_shutdown)
        except Exception as e:
            LOGGER.fatal(f"Address already in use {HOST} {PORT}")
            LOGGER.exception(e)
            raise

        # self.__server.allow_reuse_address = True
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        self.__server_thread = threading.Thread(target=self.__server.serve_forever, daemon=True)
        # Exit the server thread when the main thread terminates
        self.__server_thread.start()
        ip, port = self.__server.server_address
        LOGGER.info(f"{__name__} waiting at {ip}. {port}")

    def stop(self):
        if self.__already_shutting_down:
            return
        self.__already_shutting_down = True
        LOGGER.info("Shutting down %s", str(__name__))
        self.__is_shutdown.set()
        if self.__server is not None:
            self.__server.shutdown()
            self.__server.server_close()
        if self.__server_thread is not None:
            self.__server_thread.join()
        LOGGER.info("Shutdown complete %s", str(__name__))
