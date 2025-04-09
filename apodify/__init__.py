__name__ = "apodify"
__version__ = "0.1.0"

if __name__ == "__main__" or __name__ == "apodify":
    from sys import stdout
    from loguru import logger

    logger.remove()
    logger.add(
        stdout,
        colorize=True,
        format="<c>{time:YY-MM-DD.HH:mm:ss}</c> <level>{level: <8}</level> <level>{message}</level>",
    )
