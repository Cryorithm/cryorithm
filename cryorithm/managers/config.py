"""
Cryorithm™ | Managers | Config
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

import os
import yaml
from pathlib import Path


class Config:
    """
    Manages configuration settings for an application.
    
    This class loads configuration data from a specified YAML file and environment variables,
    providing a centralized access point for configuration settings.

    Layering happens in this order (last wins):
    1. Default Config
    2. YAML File Config
    3. Environment Variables Config
    3. CLI Options Config
    
    Attributes:
        path (Path): The path to the configuration file.
        data (dict): The loaded configuration data.
    """
    def __init__(self, path: str, ticker: str, destination: str, kafka_bootstrap_servers: str, kafka_topic: str):
        """
        Initializes a new instance of the Config class.
        
        Args:
            path (str): File path of the YAML configuration file.
            ticker (str): Ticker symbol for the stock.
            destination (str): Desination where signals will be sent.
        """
        self.path = Path(path)
        self.ticker = ticker
        self.destination = destination
        self.data = self._load()

    def _load(self) -> dict:
        """
        Private method to load configuration from a file and environment variables.
        
        Returns the configuration with environment variables overriding the file settings where applicable.
        """
        # Default configuration settings
        default_config = {
            "api_key": "default-openai-key",
            "kafka_bootstrap_servers": kafka_bootstrap_servers,
            "kafka_topic": ticker,
        }

        # Load and update from YAML file if it exists
        if self.path.exists():
            with self.path.open() as file:
                config_data = yaml.safe_load(file)
                defaults.update(config_data)

        # Environment variable overrides
        env_config = {
            "api_key": os.getenv("OPENAI_API_KEY", defaults["api_key"]),
            "kafka_bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", defaults["kafka_bootstrap_servers"]),
        }
        return env_config

    def get(self) -> dict:
        """
        Retrieves the loaded configuration data.
        
        Returns:
            dict: The configuration data as a dictionary.
        """
        return self.data
