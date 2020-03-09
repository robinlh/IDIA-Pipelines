import numpy as np
import psutil
import scipy.signal
import time

from datetime import datetime

num_trials = 5

# Count the number of physical CPUs.
num_cpus = psutil.cpu_count(logical=False)


# print('Using {} cores.'.format(num_cpus))

################################################
###### Benchmark 1: numerical computation ######
################################################


def f(image, random_filter):
    # Do some image processing.
    return scipy.signal.convolve2d(image, random_filter)[::5, ::5]


filters = [np.random.normal(size=(4, 4)) for _ in range(num_cpus)]


def run_benchmark():
    image = np.ones((3000, 3000))
    [f(image, filters[i]) for i in range(num_cpus)]


file = open('test.log', 'a')
file.write('Sequential code test @ {}:\n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
durations1 = []
for _ in range(num_trials):
    start_time = time.time()

    run_benchmark()

    duration1 = time.time() - start_time
    durations1.append(duration1)
    file.write('Numerical computation workload took {} seconds.\n'.format(duration1))

file.close()