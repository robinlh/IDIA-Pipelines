import simpy
import random

from components import Job, JobGenerator, Block, Processor


def main(num_nodes, num_jobs):
    # setup for reproducing results
    random.seed(42)

    # instantiate simulation objects
    env = simpy.Environment()
    block = Block(env, num_nodes)
    job_gen = JobGenerator(num_jobs)
    processor = Processor(env, block, job_gen)

    # run simulation
    env.process(processor.run_block())
    env.run()

    # get results
    print(
        'Average run time for {} jobs on {} node(s): {}s'
            .format(num_jobs, num_nodes, processor.get_average_proc_time())
    )


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
