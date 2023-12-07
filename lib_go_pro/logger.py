import logging

from rich.logging import RichHandler
from rich import traceback

logger: logging.Logger = logging.getLogger("tutorial_logger")
sh = RichHandler(rich_tracebacks=True, enable_link_path=True, show_time=False)
stream_formatter = logging.Formatter("%(asctime)s.%(msecs)03d %(message)s", datefmt="%H:%M:%S")
sh.setFormatter(stream_formatter)
sh.setLevel(logging.DEBUG)
logger.addHandler(sh)
logger.setLevel(logging.INFO)

bleak_logger = logging.getLogger("bleak")
bleak_logger.setLevel(logging.WARNING)
bleak_logger.addHandler(sh)

traceback.install()  # Enable exception tracebacks in rich logger

GOPRO_BASE_UUID = "b5f9{}-aa8d-11e3-9046-0002a5d5c51b"
GOPRO_BASE_URL = "http://10.5.5.9:8080"