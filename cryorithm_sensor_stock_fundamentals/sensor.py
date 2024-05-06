"""
Cryorithm™ | Sensor | Stock Fundamentals
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

# TODO: Make everything object oriented with factories that are easy to test and inuit about.
# TODO: Abstract yfinance out such that we can replace it very easily someday or make the source of data selectable.
# TODO: Work with any desired yfinance-supported ticker symbol.
# TODO: Implement a CLI flags to enable the sensor to post its messages to OpenAI API for summary and analysis. Include a natural language prompt requesting summary and analysis in the standard message, regardless of destination being OpenAI or Kafka.
# TODO: Implement a CLI flags to enable the sensor to post its messages to Kafka.
# TODO: Take the ticker symbol from a CLI flag.
# TODO: Take a cron-style schedule and use it to orchestrate the triggering of
#       pull->push of stock fundamentals.
# TODO: Instead of printing, output structured logs.
# TODO: Craft a json schema for the sensor status message sent onward to OpenAI and/or Kafka. Should be the same message regardless of destination (for now).
# TODO: Make everything asyncio.
# TODO: Use click but anticipate bugs that come from using asyncio.
# TODO: Take config from yaml config (OR) command line (OR) environment variables, or mix and match with eval order of yaml overridden by environment variables overridden by command line. 
# TODO: The config file that drives this sensor should live at ~/.config/cryorithm/config.yaml, and it should anticipate settings for sensors, as well as other system layers. And for sensors, it should have a key specific to this sensor only when necessary. E.g. OpenAI key should be centrally configured in that config.

import json

import openai
import yfinance as yf

# Fetch data for Ford Motor Company
ford_stock = yf.Ticker("F")

# Get stock info
info = ford_stock.info

# Convert to JSON
info_json = json.dumps(info, indent=4)

# Print JSON output.
print(info_json)
