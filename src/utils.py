import time


class Logger:
    def _log(self, message, level="INFO"):
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"{time_now} :: {level} - {message}")

    def info(self, message):
        self._log(message, "INFO")

    def error(self, message):
        self._log(message, "ERROR")

    def warning(self, message):
        self._log(message, "WARNING")

    def debug(self, message):
        self._log(message, "DEBUG")
