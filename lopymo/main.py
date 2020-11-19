import argparse
import codecs
import logging
import logging.config
import os
import signal
import threading
import time

import yaml
import zope.event
from . import log_cpu_mem_usage


from .data_models import shutdown_event
from .utils import get_session_folder

LOGGER = logging.getLogger(__name__)


def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration

    """
    this_dir, _ = os.path.split(__file__)
    path = os.path.join(this_dir, default_path)
    # value = os.getenv(env_key, None)
    # if value:
    #     path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


is_shutdown = threading.Event()


def stop_handler(*args):
    #del signal_received, frame
    LOGGER.info("")
    LOGGER.info("=============================================")
    LOGGER.info("Bradcasting global shutdown from stop_handler")
    LOGGER.info("=============================================")
    #zope.event.notify(shutdown_event.ShutdownEvent("KeyboardInterrupt received"))
    global is_shutdown
    is_shutdown.set()


def raise_unhandled_exeception_error():
    LOGGER.info("")
    LOGGER.info("=============================================")
    LOGGER.info("Bradcasting unhandled exception error")
    LOGGER.info("=============================================")
    zope.event.notify(shutdown_event.ShutdownEvent("Unhandled global exception"))
    global is_shutdown
    is_shutdown.set()


def init_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='VA server')
    parser.add_argument('--app', type=int, help="Analytics id, e.g. 207")
    parser.add_argument('--input', help="Input url, e.g. D:/monotosh_todelete/AERunner_base2/video/7.AVI")
    parser.add_argument('--uid', help="Input uid, e.g. admin")
    parser.add_argument('--passwd', help="pass, e.g. admin")

    return parser



def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()

def get_version():
    return read("VERSION")


def main():

    signal.signal(signal.SIGINT, stop_handler)
    signal.signal(signal.SIGTERM, stop_handler)
    print("Using session {}".format(get_session_folder()))
    setup_logging()
    LOGGER.info("=============================================")
    LOGGER.info("              Started  {} {}               ".format(__name__, get_version()))
    LOGGER.info("=============================================")
    print("Using session {}".format(get_session_folder()))
    x = shutdown_event.ShutdownEvent("KeyboardInterrupt received")
    print(x)
    try:
        parser = init_argparser()
        args = parser.parse_args()
        if args.input is not None:
            pass

        l = log_cpu_mem_usage.LogCpuMemUsage()
        l.start()
        global is_shutdown
        while not is_shutdown.wait(10.0):
            continue
        l.stop()
    except Exception as e:
        LOGGER.exception(e)
        # LOGGER.fatal(e)
        raise_unhandled_exeception_error()

    LOGGER.info("=============================================")
    LOGGER.info("              Shutdown complete {} {}               ".format(__name__, get_version()))
    LOGGER.info("=============================================")


