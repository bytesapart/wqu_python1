import sys
import logging
import matplotlib
import matplotlib.pyplot as plt

from copy import deepcopy
from optparse import OptionParser

# User defined library imports
from exsmooth import get_timeseries_data, expo_smoothening
from linearregress import perform_linear_regression

# Define some constants that will be used in our program. This makes it easier to change
# them and get different results on the fly
_TICKER = 'AAPL'


def bootstrap_logging():
    """
    This function sets up the logging level
    The logging level is as passed in the console 
    
    :return: None
    """
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m-%d-%Y %H:%M:%S',
                        level=logging.ERROR)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)


def driver():
    usage = "usage: %prog [options] --csv name_of_file.csv"
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--csv", dest="csv_filename",
                      help="A csv file containing the values", default=None)
    opts = vars(parser.parse_args()[0])

    # Get the Timeseries Data
    data_df = get_timeseries_data(opts['csv_filename'], _TICKER)

    # prompt the user for an alpha value to perform expo smoothening
    user_input = 'n'
    while user_input.lower() == 'n':
        expo_df = deepcopy(data_df)
        alpha = float(input('Please enter an alpha value for Exponential Smoothening: '))
        # Perform Exponential Smoothening
        expo_df = expo_smoothening(expo_df, alpha)

        # Print out the matplotlib timeseries
        matplotlib.style.use('ggplot')
        expo_df.plot(kind='line', title='Default vs Exponential Smoothed').legend(labels=['Default Value (Open)',
                                                                                          'Exponential Smoothed'])
        plt.show()

        user_input = input('Was this model appropriate? [Y/n]: ')
        if user_input.lower() == 'y':
            break
        elif user_input.lower() == 'n':
            continue
        else:
            print('Assuming "n"')
            user_input = 'n'

    # Perform Linear Regression
    perform_linear_regression(deepcopy(data_df))

if __name__ == '__main__':
    '''
    This is the part that gets executed when the script is called
    '''
    # Bootstrap logging levels, to enable better debgging
    bootstrap_logging()
    # Call the driver function, which will drive the program
    driver()
    logging.debug('The program is about to exit gracefully')
    sys.exit(0)
