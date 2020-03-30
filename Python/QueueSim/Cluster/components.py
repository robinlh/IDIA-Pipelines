import simpy
import random
import statistics
import logging
from functools import wraps

processing_times = []


# decorator class for logging
class Logger:
    def __init__(self, original_function):
        self.original_function = original_function
        logging.basicConfig(filename='{}.log'.format(self.original_function.__name__), level=logging.INFO)

    def __call__(self, *args, **kwargs):
        env, job, block = args
        logging.info(
            'nodes/capacity: {}/{}\nrequests: {}\nqueued events: {}'
            .format(block.nodes.count, block.nodes.capacity, len(block.nodes.users), len(block.nodes.queue))
        )
        return self.original_function(*args, **kwargs)


class Job:
    def __init__(self, job_id, size):
        """
        :param job_id:
        :param size: size of job in units (for now use abstract single units)
        """
        self.job_id = job_id
        self.size = size

    def __repr__(self):
        print('job: {} size: {}'.format(self.job_id, self.size))


# class JobGenerator:
#     def __init__(self):


class Block:
    def __init__(self, env, num_nodes):
        self.env = env
        self.nodes = simpy.Resource(env, num_nodes)

    def ingest_job(self, job):
        yield self.env.timeout(random.randint(1, 3) * job.size)

    def compute_job(self, job):
        yield self.env.timeout(random.randint(1, 5) * job.size)


@Logger
def process_job(env, job, block):
    arrival_time = env.now

    # print_stats(block.nodes)
    with block.nodes.request() as request:
        yield request
        yield env.process(block.ingest_job(job))
        yield env.process(block.compute_job(job))
        # print_stats(block.nodes)

    # print_stats(block.nodes)
    processing_times.append(env.now - arrival_time)


def run_block(env, num_nodes, num_jobs):
    block = Block(env, num_nodes)

    for job_num in range(num_jobs):
        yield env.timeout(0.1)
        job = Job(job_num, random.randint(10, 12))
        env.process(process_job(env, job, block))


def get_average_proc_time(proc_times):
    return statistics.mean(proc_times)


def print_stats(resource):
    print('{} of {} slot allocated.'.format(resource.count, resource.capacity))
    print('  Users:', resource.users)
    print('  Queued events:', resource.queue)


def main(num_nodes, num_jobs):
    # setup for reproducing results
    random.seed(42)

    # run simulation
    env = simpy.Environment()
    env.process(run_block(env, num_nodes, num_jobs))
    env.run()

    # get results
    print(
        'Average run time for {} jobs on {} node(s): {}s'
            .format(num_jobs, num_nodes, get_average_proc_time(processing_times))
    )

    processing_times.clear()


if __name__ == '__main__':
    main(1, 100)
    main(2, 100)
    main(3, 100)
    main(4, 100)
    main(5, 100)
    main(6, 100)
    main(7, 100)
    main(8, 100)
    main(9, 100)
    main(10, 100)
