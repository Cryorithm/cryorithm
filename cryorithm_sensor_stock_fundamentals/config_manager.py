"""
Cryorithm™ | Config Manager
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

def load_config(path: Path) -> dict:
    default_config = {
        'api_key': 'default-openai-key',
        'kafka_bootstrap_servers': 'localhost:9092',
        'kafka_topic': 'stock_sensor'
    }

    if path.exists():
        with path.open() as file:
            file_config = yaml.safe_load(file)
            default_config.update(file_config)

    config_from_env = {
        'api_key': os.getenv('OPENAI_API_KEY', default_config['api_key']),
        'kafka_bootstrap_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', default_config['kafka_bootstrap_servers'])
    }
    
    return config_from_env
