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
# TODO: Instead of printing, output structured logs. Add a LogManager that natively handles structured logging.
# TODO: Craft a json schema for the sensor status message sent onward to OpenAI and/or Kafka. Should be the same message regardless of destination (for now).
# TODO: Ensure the help text gives accurate first and second level defaults. (see: topic -> ticker)
# TODO: Allow override of default log file location via Click. 


import asyncio
import json

from pathlib import Path

import click

from cryorithm.clients.kafka import KafkaClientWrapper
from cryorithm.clients.openai import OpenAIClientWrapper
from cryorithm.managers.config import ConfigManager
from cryorithm.managers.log import LogManager
from cryorithm.sensors.stock.fundamentals import StockFundamentalsSensor

@click.command()
@click.option('--config-path',
        type=click.Path(),
        default='~/.config/cryorithm/config.yaml',
        show_default=True,
        envvar='CRYORITHM_CONFIG_PATH',
        help='Path to the configuration YAML file.')  
@click.option('--ticker',
        help='Stock ticker symbol.')
@click.option('--destination',
        type=click.Choice(['kafka', 'log', 'openai']),
        help='Destination system where signals will be sent.')
@click.option('--kafka-bootstrap-servers',
        help='Kafka bootstrap servers connection string.')
@click.option('--kafka-topic',
        help='Kafka topic where signals are sent.')
def main(config_path, ticker, destination, kafka_bootstrap_servers, kafka_topic):

    # Initialize config manager
    conf_manager = ConfigManager()

    # Initialize log manager
    log_manager.info("Application started", event="startup")
    log_manager = LogManager(log_level="INFO", log_file="cryorithm.log")
    log_manager = LogManager(log_config)


"""EXAMPLES

    # Demonstrate logging
    log_manager.info("Application started")
    log_manager.warning("This is a warning")
    log_manager.error("An error occurred")
    log_manager.critical("Critical issue")

    try:
        # Your application logic here
        log_manager.debug("Processing data: %s", data)
    except Exception as e:
        log_manager.error("An error occurred: %s", e)
"""

    # Load configurations in predefined order
    conf_manager.load_yaml(config_path)
    conf_manager.load_env_vars()
    
    # Prepare CLI arguments before passing them to update_from_cli
    cli_args = {
        'ticker': ticker,
        'destination': destination,
        'kafka_bootstrap_servers': kafka_bootstrap_servers,
        'kafka_topic': kafka_topic
    }
    
    conf_manager.update_from_cli(cli_args)
    config = conf_manager.get_config()  # Returns the final version of the config.
   
    # TODO: Structured log output the config here, but mask the OpenAI API Key.
    print(config)

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
            openai_client_wrapper = OpenAIClientWrapper(api_key=config[["openai"]["api_key"])
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
