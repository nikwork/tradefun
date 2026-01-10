import logging


class BaseClient:
    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )
