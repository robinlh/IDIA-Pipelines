import logging
from functools import wraps


# this library will contain utility functions for logging
# the following decorator is built purely for the process_block() method in the Processor class
# methods will become more general

def log_resource_stats(resource):
    """
    :param resource: the type of resource object passed in as a string e.g. 'block'
    :return: class method decorator
    """

    def decorator(original_function):
        logging.basicConfig(filename='{}.log'.format(original_function.__name__), level=logging.INFO)

        @wraps(original_function)
        def wrapper(self, *args, **kwargs):
            block = getattr(self, resource)
            # log before running function
            logging.info(
                'nodes/capacity: {}/{}\nrequests: {}\nqueued events: {}'
                    .format(block.nodes.count, block.nodes.capacity, len(block.nodes.users), len(block.nodes.queue))
            )
            x = original_function(self, *args, **kwargs)

            # log after as well
            logging.info(
                'nodes/capacity: {}/{}\nrequests: {}\nqueued events: {}'
                    .format(block.nodes.count, block.nodes.capacity, len(block.nodes.users),
                            len(block.nodes.queue))
            )
            return x
        return wrapper
    return decorator
