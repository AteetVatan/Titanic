"""Module For Creating Histogram."""
import sys
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')


def create_histogram(data_list: []):
    """    
    Function creates histogram for given data
    """
    plt.hist(data_list)
    plt.show()
    plt.savefig(sys.stdout.buffer)
    sys.stdout.flush()
