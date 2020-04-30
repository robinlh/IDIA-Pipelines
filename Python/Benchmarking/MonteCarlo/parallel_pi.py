import numpy as np
from mpi4py import MPI
import logging
import time

from socket import gethostname


# from utilities import log_function_execution_time


def generate_points(num_points):
    """
    generate uniformly random points that lie within square with corners at (-1,-1),
    (-1,1), (1,1), (1,-1)
    :param num_points: number of (x, y) points to generate
    :return: array of n uniformly random (x, y) pairs
    """
    return 2 * np.random.random((num_points, 2)) - 1


def is_point_in_circle(point_array):
    """
    returns boolean array of True/False elements whether point in circle.
    Circle has radius one, therefore can use np.linalg.norm to get vector from origin
    to point and compare to the radius of 1.
    :param point_array: an array of (x, y) points
    :return: boolean array
    """
    return np.linalg.norm(point_array, axis=-1) <= 1.0


def estimate_pi(point_array):
    """
    return the estimate of pi from fraction of points within circle
    :param point_array: array of uniform randomly generated (x, y) points
    :return: float estimation of pi
    """
    in_circle = np.sum([is_point_in_circle(point) for point in point_array])
    return in_circle / len(point_array) * 4.


def chunk_points(point_array, num_chunks):
    """
    split point array into specified number of successive chunks
    :param point_array: array of uniform randomly generated (x, y) points
    :param num_chunks: number of chunks to split into
    :return: numpy array of arrays
    """
    return np.array_split(point_array, num_chunks)


def estimate_pi_parallel(size, rank, comm, point_array):
    """
    Split point array into chunks to be scattered to workers
    :param comm:
    :param rank:
    :param size:
    :param point_array:
    :return: average of pi estimates for all chunks
    """

    if rank == 0:
        data = chunk_points(point_array, size)
    else:
        data = None

    data = comm.scatter(data, root=0)
    pi_estimate = estimate_pi(point_array)
    pi_estimates = comm.gather(pi_estimate, root=0)

    if rank == 0:
        return np.mean(pi_estimates)


def main(size, rank, comm, point_array):
    """
    :param size:
    :param rank:
    :param comm:
    :param point_array:
    :return:
    """
    logging.basicConfig(filename='parallel.'+str(rank)+'.log', level=logging.INFO)
    logging.info('This is rank ' + str(rank) + ' running on ' + gethostname())
    if rank == 0:
        logging.info('run with {} cores'.format(size))

    if size > 1:
        t1 = MPI.Wtime()
        pi = estimate_pi_parallel(size, rank, comm, point_array)
        t2 = MPI.Wtime() - t1
        if rank == 0:
            logging.info('Pi: {}\ntime (s): {}'.format(pi, t2))
    else:
        t1 = time.time()
        pi = estimate_pi(point_array)
        t2 = time.time() - t1
        logging.info('Pi: {}\ntime (s): {}'.format(pi, t2))


if __name__ == '__main__':
    np.random.seed(999)
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    points = generate_points(5000)
    main(size, rank, comm, points)
