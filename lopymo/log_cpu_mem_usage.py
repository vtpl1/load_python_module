from threading import Thread, Event
import logging
import psutil
import zope.event
from .data_models import shutdown_event

LOGGER = logging.getLogger(__name__)
LOGGER_CPU_USAGE = logging.getLogger("cpu_usage")


class LogCpuMemUsage(Thread):
    """
    Log CPU and memory usage
    """

    def __init__(self):
        self.__is_stop = Event()
        self.__is_already_shutting_down = False
        zope.event.subscribers.append(self.global_shutdown_handler)
        super().__init__()

    def global_shutdown_handler(self, event):
        if isinstance(event, shutdown_event.ShutdownEvent):
            LOGGER.info("Global shutdown received %s", str(event.reason))
            self.stop()

    def run(self) -> None:
        LOGGER_CPU_USAGE.info("============== Start ================")
        LOGGER_CPU_USAGE.info(
            "Cores: {} Frequency: {} Mem: {} GB {}".format(
                psutil.cpu_count(),
                psutil.cpu_freq(),
                psutil.virtual_memory().total / (1024 * 1024 * 1024),
                psutil.sensors_temperatures(),
            )
        )
        LOGGER_CPU_USAGE.info("CPU Percentage, MEM Percentage")
        while True:
            LOGGER_CPU_USAGE.info(
                "{:6.1f}, {:6.1f}".format(
                    psutil.cpu_percent(),
                    psutil.virtual_memory().percent,
                )
            )
            if self.__is_stop.wait(10.0):
                break
            else:
                continue
        LOGGER_CPU_USAGE.info("============== End   ================")

    def stop(self):
        if self.__is_already_shutting_down:
            return
        self.__is_already_shutting_down = True
        zope.event.subscribers.remove(self.global_shutdown_handler)
        self.__is_stop.set()

    def __del__(self):
        self.stop()