"""
Cryorithm™ | CLI
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

# TODO: Move to a Poetry mono repo for the v1 architecture.
# TODO: Take a cron-style schedule and use it to orchestrate the triggering of
#       pull->push of stock fundamentals.
# TODO: Instead of printing, output structured logs.
# TODO: Craft a json schema for the sensor status message sent onward to OpenAI and/or Kafka. Should be the same message regardless of destination (for now).

import asyncio
import json
from pathlib import Path

import click

import cryorithm as cryo


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
    config = cryo.config.load(Path(config_path).expanduser())
    sensor = cryo.sensor.stock.fundamentals.Sensor(ticker)
    asyncio.run(job(sensor, destination, config))


async def job(sensor: StockSensor, destination: str, config):
    data = await sensor.fetch_data()

    if data:
        if destination == "openai":
            client_wrapper = cryo.openai.OpenAIClientWrapper(api_key=config["api_key"])
            async for message in client_wrapper.create_chat_completion_stream(
                model=config["model_name"],
                messages=[{"role": "user", "content": data}],
            ):  # Assuming 'data' is directly usable here; may need formatting.
                print(
                    message,
                )  # Consider processing or further handling of the response.

        elif destination == "kafka":
            await cryo.kafka.publish(json.dumps(data), config)

    else:
        print("Failed to fetch data")


if __name__ == "__main__":
    main()
