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

# TODO: Take a cron-style schedule and use it to orchestrate the triggering of
#       pull->push of stock fundamentals.
# TODO: Instead of printing, output structured logs.
# TODO: Craft a json schema for the sensor status message sent onward to OpenAI and/or Kafka. Should be the same message regardless of destination (for now).
# TODO: Make everything asyncio.

import asyncio
import click
from pathlib import Path

from cryorithm_sensor_stock_fundamentals.config_manager import load_config
from cryorithm_sensor_stock_fundamentals.stock_sensor import StockSensor
from cryorithm_sensor_stock_fundamentals.openai_client import call_openai_api
from cryorithm_sensor_stock_fundamentals.kafka_client import send_to_kafka


@click.command()
@click.option("--ticker", required=True, help="Ticker symbol for stock.")
@click.option(
    "--destination",
    type=click.Choice(["kafka", "openai"]),
    required=True,
    help="Destination where the messages will be sent.",
)
@click.option(
    "--config-path",
    default="~/.config/cryorithm/config.yaml",
    help="Path to configuration YAML file.",
)
def main(ticker, destination, config_path):
    global config
    config = load_config(Path(config_path).expanduser())

    sensor = StockSensor(ticker)

    asyncio.run(job(sensor, destination))


async def job(sensor: StockSensor, destination: str):
    data = await sensor.fetch_data()
    if data is not None:
        if destination == "openai":
            await call_openai_api(data, config["api_key"])
        elif destination == "kafka":
            await send_to_kafka(json.dumps(data), config)
    else:
        print("Failed to fetch data")


if __name__ == "__main__":
    main()
