import numpy as np
import logging


class Simulation:
    def __init__(self):
        # number of events being processed currently
        self.num_in_system = 0

        # total system clock
        self.clock = 0.0

        self.t_arrival = self.generate_interarrival()
        self.t_depart = float('inf')

        self.num_arrivals = 0
        self.num_departs = 0
        self.total_wait = 0.0

    def advance_time(self):
        """handle incrementing all time statistics"""

        # smaller of next arrival or next departure to determine the time next event takes
        t_event = min(self.t_arrival, self.t_depart)

        # increase total sim time
        self.total_wait += self.num_in_system * (t_event - self.clock)

        # move the clock forward
        self.clock = t_event

        # if next arrival event is sooner than departure event
        if self.t_arrival <= self.t_depart:
            self.handle_arrival_event()
        else:
            self.handle_depart_event()

    def handle_arrival_event(self):
        self.num_in_system += 1
        self.num_arrivals += 1

        # if only one event in system next departure time must be scheduled
        if self.num_in_system <= 1:
            self.t_depart = self.clock + self.generate_service()
        self.t_arrival = self.clock + self.generate_interarrival()

    def handle_depart_event(self):
        self.num_in_system -= 1
        self.num_departs += 1

        # if there are still events to process, set next departure time
        # otherwise set to infinity
        if self.num_in_system > 0:
            self.t_depart = self.clock + self.generate_service()
        else:
            self.t_depart = float('inf')

    def generate_interarrival(self):
        return np.random.exponential(1. / 3)

    def generate_service(self):
        return np.random.exponential(1. / 4)


np.random.seed(0)

sim = Simulation()


def log_info(simulation):
    logging.info(
        'system events: {}\ntime elapsed: {}\ndepartures: {}\narrivals: {}'
        .format(simulation.num_in_system, simulation.clock, simulation.num_departs, simulation.num_arrivals)
    )


logging.basicConfig(filename='{}.log'.format(log_info.__name__), level=logging.INFO)
for i in range(1000):
    sim.advance_time()
    log_info(sim)
