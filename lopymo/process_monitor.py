

import logging
from threading import Event, Thread

from .data_models import shutdown_event

LOGGER = logging.getLogger(__name__)


class ProcessMonitor(Thread):
    def __init__(self) -> None:
        self.__is_stop = Event()
        self.__is_already_shutting_down = False
        super().__init__()

    def global_shutdown_handler(self, event) -> None:
        if isinstance(event, shutdown_event.ShutdownEvent):
            LOGGER.info("Global shutdown received %s", str(event.reason))
            self.stop()

    def run(self) -> None:
        LOGGER.info("============== Start ================")
        while True:
            if self.__is_stop.wait(10.0):
                break
            else:
                continue
        LOGGER.info("============== End   ================")

    def stop(self) -> None:
        if self.__is_already_shutting_down:
            return
        self.__is_already_shutting_down = True
        self.__is_stop.set()

    def __del__(self):
        self.stop()
