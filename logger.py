import logging
from colorama import Back, Fore, Style, init

init(autoreset=True)


def get_logger():
    class ColoredFormatter(logging.Formatter):
        def format(self, record):
            level_color = f"{record.levelname}{Style.RESET_ALL}"
            timestamp = self.formatTime(record, datefmt="%H:%M:%S %d-%b-%y")
            message = record.getMessage()
            message_color = {
                logging.DEBUG: Fore.BLUE,
                logging.INFO: Fore.GREEN,
                logging.WARNING: Fore.YELLOW,
                logging.ERROR: Fore.RED,
                logging.CRITICAL: Fore.RED,
            }.get(record.levelno, "")
            return f"{timestamp} - {level_color}: {message_color}{message}{Style.RESET_ALL}"

    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()

    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)

    logging.addLevelName(logging.DEBUG, f"{Fore.BLUE}DEBUG{Style.RESET_ALL}")
    logging.addLevelName(logging.INFO, f"{Fore.GREEN}INFO{Style.RESET_ALL}")
    logging.addLevelName(
        logging.WARNING, f"{Fore.YELLOW}{Style.BRIGHT}WARNING{Style.RESET_ALL}"
    )
    logging.addLevelName(
        logging.ERROR, f"{Fore.RED}{Style.BRIGHT}ERROR{Style.RESET_ALL}"
    )
    logging.addLevelName(
        logging.CRITICAL,
        f"{Fore.WHITE}{Style.BRIGHT}{Back.RED} CRITICAL {Style.RESET_ALL}",
    )

    return logger
