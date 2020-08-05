import datetime
from modules.Config import Config
import os

class FileNotFoundException(Exception):
    pass

class Logger:
    def __init__(self, config: Config):
        self.config = config
    
    def _writeToFile(self, msg: str):
        if not os.path.isdir(self.config.get("log_file")):
            with open(self.config.get("log_file"), "a") as file:
                file.write(msg + "\n")
        else:
            raise FileNotFoundException("Cannot write to directory! " + self.config.get("log_file"))


    def _getDateTimeNow(self):
        return datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    
    def warning(self, message: str) -> bool:
        output = "[" + self._getDateTimeNow() + "] "
        output += "WARNING: " + str(message)
        self._writeToFile(output)
        return True

    def info(self, message: str) -> bool:
        output = "[" + self._getDateTimeNow() + "] "
        output += "INFO: " + str(message)
        self._writeToFile(output)
        return True

    def fatal(self, message: str) -> bool:
        output = "[" + self._getDateTimeNow() + "] "
        output += "FATAL: " + str(message)
        self._writeToFile(output)
        return True

    def success(self, message: str) -> bool:
        output = "[" + self._getDateTimeNow() + "] "
        output += "SUCCESS: " + str(message)
        self._writeToFile(output)
        return True