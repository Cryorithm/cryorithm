"""
Cryorithm™ | Managers | Job
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

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from apscheduler.triggers.cron import CronTrigger


class JobManager:
    """
    Manages scheduling and execution of jobs for sensors using cron expressions.

    This class utilizes APScheduler (Advanced Python Scheduler) library for
    scheduling jobs based on sensor-specific cron expressions and the `asyncio`
    library for running asynchronous data fetching tasks.

    Attributes:
        sensors (list): A list of sensor objects that provide data fetching
            functionality and cron schedule information.
        log_manager (LogManager): An instance of the LogManager class
            for logging messages related to job scheduling and execution.
        scheduler (AsyncIOScheduler): An instance of the APScheduler for
            managing cron-based job scheduling.
    """

    def __init__(self, sensors: list, log_manager: "LogManager"):
        """
        Initializes the JobManager with sensor data and a LogManager instance.

        Args:
            sensors (list): A list of sensor objects.
            log_manager (LogManager): An instance of the LogManager class
                for logging purposes.
        """

        self.sensors = sensors
        self.log_manager = log_manager
        self.scheduler = AsyncIOScheduler()

    async def start_jobs(self):
        """
        Schedules jobs for each sensor based on their cron expressions.

        This method iterates through the list of sensors and schedules an
        asynchronous job using APScheduler for each sensor. The job is defined
        to call the `job` function with the sensor as an argument at the
        specified cron schedule time. Logs a message for each scheduled job
        using the LogManager.
        """

        for sensor in self.sensors:
            trigger = CronTrigger(cron=sensor.schedule_time)
            self.scheduler.add_job(self.job, trigger, args=[sensor])
            self.log_manager.info(f"Scheduled job for {sensor.name} with cron: {sensor.schedule_time}")

        await self.scheduler.start()

    @staticmethod
    async def job(sensor):
        """
        Asynchronous job function to fetch data from a sensor.

        This function attempts to fetch data from the provided sensor using
        the sensor's `fetch_data` method. If data is successfully fetched,
        it logs the data using the LogManager and allows for further processing
        or forwarding as needed by your application.

        In case of any exceptions during data fetching, it logs an error message
        using the LogManager.

        Args:
            sensor: The sensor object for which to fetch data.

        Returns:
            None
        """

        try:
            data = await sensor.fetch_data()
            if data:
                self.log_manager.info(f"Data fetched from {sensor.name}: {data}")
                # Further process or forward this data according to your application needs.

        except Exception as e:
            self.log_manager.error(f"Error fetching data from {sensor.name}: {str(e)}")

    async def run_continuously(self):
        """
        Continuously monitors the scheduler for scheduled jobs.

        This method awaits tasks scheduled by APScheduler to run and allows
        them to execute asynchronously.
        """

        await self.scheduler.wait_closed()
