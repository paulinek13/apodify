import colorama
import logging

colorama.init(autoreset=True)


def _init_logger():
    class ColoredFormatter(logging.Formatter):
        def format(self, record):
            level_color = f"{record.levelname}{colorama.Style.RESET_ALL}"
            timestamp = self.formatTime(record, datefmt="%H:%M:%S %d-%b-%y")
            message = record.getMessage()
            message_color = {
                logging.DEBUG: colorama.Fore.BLUE,
                logging.INFO: colorama.Fore.GREEN,
                logging.WARNING: colorama.Fore.MAGENTA,
                logging.ERROR: colorama.Fore.RED,
                logging.CRITICAL: colorama.Fore.RED,
            }.get(record.levelno, "")
            return f"{timestamp} - {level_color}: {message_color}{message}{colorama.Style.RESET_ALL}"

    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter())

    logger.addHandler(console_handler)

    logging.addLevelName(
        logging.DEBUG,
        f"{colorama.Fore.BLUE}{colorama.Style.BRIGHT}DEBUG{colorama.Style.RESET_ALL}",
    )
    logging.addLevelName(
        logging.INFO,
        f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}INFO{colorama.Style.RESET_ALL}",
    )
    logging.addLevelName(
        logging.WARNING,
        f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}WARNING{colorama.Style.RESET_ALL}",
    )
    logging.addLevelName(
        logging.ERROR,
        f"{colorama.Fore.RED}{colorama.Style.BRIGHT}ERROR{colorama.Style.RESET_ALL}",
    )
    logging.addLevelName(
        logging.CRITICAL,
        f"{colorama.Fore.WHITE}{colorama.Style.BRIGHT}{colorama.Back.RED} CRITICAL {colorama.Style.RESET_ALL}",
    )

    return logger


logger = _init_logger()
