import time
from enum import Enum


class TimeUnit(Enum):
    SECONDS = 1e9
    MILLISECONDS = 1e6
    MICROSECONDS = 1e3
    NANOSECONDS = 1


class Stopwatch:
    def __init__(self, time_unit: TimeUnit):
        self.time_unit = time_unit
        self.is_running = False
        self.start_time = 0
        self.end_time = 0

    def start(self):
        if self.is_running:
            raise RuntimeError("Stopwatch is already running.")
        self.start_time = time.perf_counter_ns()
        self.is_running = True

    def stop(self):
        if not self.is_running:
            raise RuntimeError("Stopwatch is already stopped.")
        self.end_time = time.perf_counter_ns()
        self.is_running = False

    def restart(self):
        self.start_time = time.perf_counter_ns()
        self.end_time = 0
        self.is_running = True

    def print(self):
        print(self)

    def __str__(self):
        if not self.is_running and self.start_time == 0:
            return "Stopwatch has not been started yet."
        if self.is_running:
            elapsed = (time.perf_counter_ns() - self.start_time) / self.time_unit.value
            return f"Current Elapsed time: {elapsed:.9f} {self.time_unit.name.lower()}."
        else:
            elapsed = (self.end_time - self.start_time) / self.time_unit.value
            return f"Elapsed time: {elapsed:.9f} {self.time_unit.name.lower()}."
