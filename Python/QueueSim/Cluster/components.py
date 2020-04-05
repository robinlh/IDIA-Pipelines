import statistics
import simpy
import random

from utilities import log_resource_stats


class Job:
    """
    Job class is simply an information carrier
    """

    def __init__(self, job_id, size):
        """
        :param job_id: unique job id
        :param size: size of job in units (for now use abstract single units)
        """
        self.job_id = job_id
        self.size = size

    def __repr__(self):
        print('job: {} size: {}'.format(self.job_id, self.size))


class JobGenerator:
    """
    Used to generate a specified number of jobs to be sent on to a Block.
    Later will implement a continuous stream
    """

    def __init__(self, num_jobs):
        """
        :param num_jobs: number of jobs to be created
        """
        self.num_jobs = num_jobs

    def generate(self):
        for job_num in range(self.num_jobs):
            yield Job(job_num, random.randint(10, 12))


class Block:
    """
    Block class encapsulates resource allocation
    make use of dependency injection here to keep block objects doing all the work for jobs
    """

    def __init__(self, env, num_nodes):
        """
        :param env: SimPy environment to be run in
        :param num_nodes: number of nodes available
        """
        self.env = env
        self.nodes = simpy.Resource(env, num_nodes)

    # method to model inter arrival time
    def ingest_job(self, job):
        yield self.env.timeout(random.randint(1, 3) * job.size)

    # service time
    def compute_job(self, job):
        yield self.env.timeout(random.randint(1, 5) * job.size)


class Processor:
    """
    Processor class brings everything together, having jobs consume resources from the block
    later will be possible to give jobs more complex attributes to be passed into the blocks
    """

    def __init__(self, env, block, job_generator):
        """
        :param env: SimPy environment
        :param block:
        :param job_generator:
        """
        self.env = env
        self.block = block
        self.job_generator = job_generator
        self.processing_times = []

    # process a single job. Include arrival and service time
    # add processing time to list
    @log_resource_stats('block')
    def process_job(self, job):
        arrival_time = self.env.now
        with self.block.nodes.request() as request:
            yield request
            yield self.env.process(self.block.ingest_job(job))
            yield self.env.process(self.block.compute_job(job))

        self.processing_times.append(self.env.now - arrival_time)

    # run the given block
    # Note: timeout before processing could also be inter arrival time
    def run_block(self):
        for job in self.job_generator.generate():
            yield self.env.timeout(0.1)
            self.env.process(self.process_job(job))

    # put some statistics in the list
    # for debugging purposes
    # method will most likely be removed in favour of decorator
    def get_average_proc_time(self):
        return statistics.mean(self.processing_times)
