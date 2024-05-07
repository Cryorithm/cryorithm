"""
Cryorithm™ | CLI | Main
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

import asyncio
import json

from pathlib import Path

import click

from cryorithm.clients.kafka import KafkaClientWrapper
from cryorithm.clients.openai import OpenAIClientWrapper
from cryorithm.managers.config import ConfigManager
from cryorithm.sensors.stock.fundamentals import StockFundamentalsSensor

DEFAULT_CONFIG                  = '~/.config/cryorithm/config.yaml'
DEFAULT_TICKER                  = 'DASH'  # Doordash
DEFAULT_DESTINATION             = 'log'
DEFAULT_KAFKA_BOOTSTRAP_SERVERS = 'localhost:9902'
DEFAULT_KAFKA_TOPIC             = 'cryorithm'

@click.option(
    '--config',
    type=click.Path(exists=True),
    envvar='CRYORITHM_CONFIG',
    default=DEFAULT_CONFIG,
    help=f"""Path to the configuration YAML file. Can also be set via CRYORITHM_CONFIG
    environment variable. If neither flag nor environment variable is set, default
    value is: {DEFAULT_CONFIG}""",
)
@click.option(
    '--ticker',
    envvar='CRYORITHM_TICKER',
    default=DEFAULT_TICKER,
    help=f"""Stock ticker symbol. Can also be set via CRYORITHM_TICKER environment
    variable. If neither flag nor environment variable is set, default value is:
    {DEFAULT_TICKER}""",
)
@click.option(
    '--destination',
    type=click.Choice(['kafka', 'log', 'openai']),
    envvar='CRYORITHM_DESTINATION',
    default=DEFAULT_DESTINATION,
    help=f"""Destination system where signals will be sent. Can also be set via
    CRYORITHM_DESTINATION environment variable. If neither flag nor environment
    variable is set, default value is: {DEFAULT_DESTINATION}""",
)
@click.option(
    '--kafka-bootstrap-servers',
    type=click.Choice(['kafka', 'log', 'openai']),
    envvar='CRYORITHM_DESTINATION',
    default=DEFAULT_KAFKA_BOOTSTRAP_SERVERS,

    help=f"""(comma-separated list of host:port): This argument specifies a
    comma-separated list of host and port pairs of the Kafka brokers in the cluster.
    The client will initially connect to these bootstrap servers to discover the full
    set of brokers in the cluster. You can specify multiple bootstrap servers to
    provide redundancy in case one server is unavailable. Can also be set via
    CRYORITHM_KAFKA_BOOTSTRAP_SERVERS envrionment variable. If neither flag nor
    environment variable is set, default value is:
    {DEFAULT_KAFKA_BOOTSTRAP_SERVERS}""",
)
@click.option(
    '--kafka-topic',
    default=lambda ctx: ctx.params.get('ticker'),
    help=f"""Kafka topic where signals are sent, if "kafka" is the destination.
    Defaults to the final value of ticker if ticker is set. If ticker is not set,
    the default value is: {DEFAULT_KAFKA_TOPIC}""",
    callback=lambda ctx, param, value: value if value else DEFAULT_KAFKA_TOPIC,
)
default main(args):


    # By this time, the following config layers have been handled:
    # 1. Static Defaults
    # 2. Environment Variables
    # 3. CLI Flags

    # So how do I 


    config_manager = ConfigManger()
    config_manager.load_yaml('???')
    config.load_env_vars()



def main(ticker, destination, config_path):
    config = ConfigManager()
    config.load_yaml(



    # Initialize config
    cli_options_config = {
        'config_path': Path(config_path).expandus:er()
        'destination': destination,
        'kafka_bootstrap_servers': kafka_bootstrap_servers,
        'kafka_topic': kafka_topic,
        'ticker': ticker,
    }
    config_manager = ConfigManager(Path(config_path).expandus:er(), ticker, destination)
    config = config_manager.get()

    # Initialize sensors
    stock_fundamentals_sensor = StockFundamentalsSensor(ticker)
    sensors = [
        stock_fundamentals_sensor,
    ]

    # Run
    asyncio.run(job(sensors, destination, config))


async def job(sensor: StockSensor, destination: str, config):
    data = await sensor.fetch_data()

    if data:
        if destination == "openai":
            openai_client_wrapper = OpenAIClientWrapper(api_key=config["api_key"])
            async for message in client_wrapper.create_chat_completion_stream(
                model=config["model_name"],
                messages=[{"role": "user", "content": data}],
            ):  # Assuming 'data' is directly usable here; may need formatting.
                print(
                    message,
                )  # Consider processing or further handling of the response.
        elif destination == "kafka":
            await cryo.kafka.publish(json.dumps(data), config)
        elif destination == "log":
            print(json.dumps(data))

    else:
        print("Failed to fetch data")


if __name__ == "__main__":
    main()
