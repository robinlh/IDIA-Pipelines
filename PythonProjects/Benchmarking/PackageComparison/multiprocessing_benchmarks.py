from multiprocessing import Pool, cpu_count
import numpy as np
import scipy.signal
import time


from datetime import datetime

num_trials = 5

# Count the number of physical CPUs.
num_cpus = cpu_count()


# print('Using {} cores.'.format(num_cpus))


## NUMERICAL BENCHMARK SIM ##

def f(args):
    image, random_filter = args
    # Do some image processing.
    return scipy.signal.convolve2d(image, random_filter)[::5, ::5]


pool = Pool(num_cpus)
# print(pool)

filters = [np.random.normal(size=(4, 4)) for _ in range(num_cpus)]


# print(filters)


def run_benchmark():
    image = np.ones((3000, 3000))
    pool.map(f, zip(num_cpus * [image], filters))


file = open('test.log', 'a')
file.write('Multiprocessing code test @ {}:\n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
durations1 = []
for _ in range(num_trials):
    start_time = time.time()

    run_benchmark()

    duration1 = time.time() - start_time
    durations1.append(duration1)
    file.write('Numerical computation workload took {} seconds.\n'.format(duration1))

file.close()
