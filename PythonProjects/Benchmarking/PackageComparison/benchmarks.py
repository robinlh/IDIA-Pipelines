import numpy as np
import scipy.signal
import time
import ray
import sys
from multiprocessing import Pool, cpu_count
from datetime import datetime


# function to perform matrix convolution
# use remote decorator when calling this function for ray operations

def convolve(args):
    image, random_filter = args
    # Do some image processing.
    return scipy.signal.convolve2d(image, random_filter)[::5, ::5]


# run benchmark function needs to be defined at the top level because multiprocessing library can't pickle nested
# functions
def run_benchmark_multi(cpu_pool, mat_filters, num_cpus, function):
    """
    :param cpu_pool: cpu pool for multiprocessing lib
    :param mat_filters: matrix filters
    :param num_cpus: number of cpus to use
    :param function: function to be mapped
    :return:
    """
    image = np.ones((3000, 3000))
    cpu_pool.map(function, zip(num_cpus * [image], mat_filters))


def multiprocessing_main(num_cpus,
                         num_trials,
                         filename):
    """
    :param filename: log file to be written to
    :param num_cpus: number of cpus to be used
    :param num_trials: number of iterations to run benchmark
    :return:
    """

    # to be implemented: sufficient cpu check

    # get available cpu pool and create filters
    pool = Pool(num_cpus)
    filters = [np.random.normal(size=(4, 4)) for _ in range(num_cpus)]

    log_file = open(filename, 'a')
    log_file.write('Multiprocessing test @ {}\n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    log_file.write('Cores: {}\n'.format(num_cpus))

    # durations = []

    for _ in range(num_trials):
        start_time = time.time()

        run_benchmark_multi(pool, filters, num_cpus, convolve)

        duration = time.time() - start_time
        # durations.append(duration)
        log_file.write('Numerical computation time (s): {}\n'.format(duration))

    log_file.close()


def ray_main(num_cpus,
             num_trials,
             filename):
    """
    same parameters as multi
    :param num_cpus:
    :param num_trials:
    :param filename:
    :return:
    """

    ray.init(num_cpus=num_cpus)
    filters = [np.random.normal(size=(4, 4)) for _ in range(num_cpus)]

    @ray.remote
    def convolve_ray(image, random_filter):
        # Do some image processing.
        return scipy.signal.convolve2d(image, random_filter)[::5, ::5]

    def run_benchmark(num_cpus):
        image = np.ones((3000, 3000))
        image_id = ray.put(image)
        ray.get([convolve_ray.remote(image_id, filters[i]) for i in range(num_cpus)])

    # Run it a couple times to warm up the Ray object store because the initial
    # memory accesses are slower.
    [run_benchmark(num_cpus) for _ in range(5)]

    log_file = open(filename, 'a')
    log_file.write('Ray test @ {}\n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    log_file.write('Cores: {}\n'.format(num_cpus))
    # durations1 = []
    for _ in range(num_trials):
        start_time = time.time()

        run_benchmark(num_cpus)

        duration = time.time() - start_time
        # durations.append(duration)
        log_file.write('Numerical computation time (s): {}\n'.format(duration))

    log_file.close()


# still need number of cpus for creating equivalent workload for sequential function
def sequential_main(num_cpus, num_trials, filename):
    """
    :param num_cpus:
    :param num_trials:
    :param filename:
    :return:
    """
    filters = [np.random.normal(size=(4, 4)) for _ in range(num_cpus)]

    def convolve_seq(image, random_filter):
        # Do some image processing.
        return scipy.signal.convolve2d(image, random_filter)[::5, ::5]

    def run_benchmark():
        image = np.ones((3000, 3000))
        [convolve_seq(image, filters[i]) for i in range(num_cpus)]

    log_file = open(filename, 'a')
    log_file.write('Sequential test @ {}\n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    log_file.write('Cores: {}\n'.format(num_cpus))
    # durations1 = []
    for _ in range(num_trials):
        start_time = time.time()

        run_benchmark()

        duration = time.time() - start_time
        # durations.append(duration)
        log_file.write('Numerical computation time (s): {}\n'.format(duration))

    log_file.close()


def run_benchmarks(num_cpus, filename, num_trials):
    cpus = int(num_cpus)
    multiprocessing_main(cpus, num_trials, filename)
    ray_main(cpus, num_trials, filename)
    sequential_main(cpus, num_trials, filename)


if __name__ == '__main__':
    run_benchmarks(sys.argv[1], sys.argv[2], 5)
# run_benchmarks(sys.argv[0], sys.argv[1], 5)
