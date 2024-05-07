"""
Cryorithm™ | Managers | Log
"""
# MIT License
#
# Copyright © 2024 Joshua M. Dotson (contact@jmdots.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from loguru import logger

class LogManager:
    def __init__(self, log_level="DEBUG", log_file=None, rotation="10 MB"):
        """
        Initializes the LogManager with logging configuration.

        Args:
            log_level (str, optional): Logging level (default: DEBUG).
            log_file (str, optional): Path to a log file (default: None).
            rotation (str, optional): Log rotation configuration for the log file (default: "10 MB").
        """
        if log_file:
            logger.add(log_file, level=log_level, rotation=rotation)
        else:
            logger.add(level=log_level)

    def debug(self, message, *args, **kwargs):
        """Logs a debug message."""
        logger.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        """Logs an informational message."""
        logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """Logs a warning message."""
        logger.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        """Logs an error message."""
        logger.error(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        """Logs a critical severity message."""
        logger.critical(message, *args, **kwargs)
