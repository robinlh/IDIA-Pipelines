import numpy as np
import psutil
import ray
import scipy.signal
import time

from datetime import datetime

num_trials = 5

# Count the number of physical CPUs.
num_cpus = psutil.cpu_count(logical=False)
print('Using {} cores.'.format(num_cpus))

ray.init(num_cpus=num_cpus)


################################################
###### Benchmark 1: numerical computation ######
################################################


@ray.remote
def f(image, random_filter):
    # Do some image processing.
    return scipy.signal.convolve2d(image, random_filter)[::5, ::5]


filters = [np.random.normal(size=(4, 4)) for _ in range(num_cpus)]


def run_benchmark():
    image = np.ones((3000, 3000))
    image_id = ray.put(image)
    ray.get([f.remote(image_id, filters[i]) for i in range(num_cpus)])


# Run it a couple times to warm up the Ray object store because the initial
# memory accesses are slower.
[run_benchmark() for _ in range(5)]

file = open('test.log', 'a')
file.write('Ray code test @ {}:\n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
durations1 = []
for _ in range(num_trials):
    start_time = time.time()

    run_benchmark()

    duration1 = time.time() - start_time
    durations1.append(duration1)
    file.write('Numerical computation workload took {} seconds.\n'.format(duration1))

file.close()
