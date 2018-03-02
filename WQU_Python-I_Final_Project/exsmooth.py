import pandas as pd
import numpy as np
import pandas_datareader.data as web
import os
import datetime as dt


def _get_data_from_google(ticker):
    """
    Get the stock data from Google Finance
    
    :param ticker: The stock ticker to fetch
    :type ticker: str
    :rtype: pd.DataFrame()
    :return: pd.DataFrame()
    """
    # If ticker is None, set it to default to AAPL
    if ticker is None:
        ticker = 'AAPL'

    # Get the 8 months from google finance
    stock_dataframe = web.DataReader(ticker, 'google', dt.date(2016, 1, 1), dt.date(2016, 8, 1))

    # Get the first of every month of the stock
    reduced_dataframe = stock_dataframe.groupby(pd.DatetimeIndex(stock_dataframe.index).to_period('M')).nth(0)

    # return the reduced dataframe
    return pd.DataFrame(reduced_dataframe['Open'])


def _create_expo_dataframe(csv_filename):
    """
    This function creates a dataframe from a CSV file. The CSV file must is validated for an
    8 datapoint time series and that the first column consit of dates, which can then be used
    as an index for the time series
    :param csv_filename: The absolute path containing the CSV file

    :type csv_filename: str

    :return: pd.DataFrame()
    """
    # Read data into dataframe
    csv_dataframe = pd.read_csv(csv_filename, header=0, index_col=0, parse_dates=True)

    # Rename the index and open column to be more consistent with Google's API
    csv_dataframe.index.names = ['Date']
    csv_dataframe.rename(columns={'open': 'Open'}, inplace=True)

    # Get the reduced set values (that is, first of every month)
    reduced_dataframe = csv_dataframe.groupby(pd.DatetimeIndex(csv_dataframe.index).to_period('M')).nth(0)

    # Return the reduced set as a DataFrame (only the top 8 values)
    return pd.DataFrame(reduced_dataframe.sort_index(ascending=True)[:8]['Open'])


def get_timeseries_data(csv_filename, ticker=None):
    """
    This function validates whether a csv_filename has been provided or not
    if not, then it assumes to take the default values from google finance

    :param csv_filename: The name of the csv file
    :param ticker: THe stock symbol

    :type csv_filename: str None
    :type ticker: str None

    :return: None
    """
    if csv_filename is None:
        while csv_filename is None:
            user_input = input('The absolute path to the CSV file has does not exist. Do you want to '
                               'accept default values (2016-01-01 to 2016-08-01) for AAPL? [Y/n]: ')
            if user_input.lower() == 'y':
                data = _get_data_from_google(ticker=ticker)
                break
            elif user_input.lower() == 'n':
                csv_filename = input('"No" option provided. Please provide an absolute path to CSV file: ')
                if not os.path.exists(csv_filename):
                    print('CSV file does not exist.')
                    csv_filename = None
                    continue
            else:
                print('Incorrect option provided. Please enter either "Y" or "n"')
                continue
    else:
        data = _create_expo_dataframe(csv_filename)

    return data


def expo_smoothening(expo_df, alpha):
    """
    This function performs exponential smoothening based on the following formulas

    :param expo_df: The Dataframe containing the TimeSeries that needs to be smoothened
    :param alpha: The alpha factor for expo smooth

    :type expo_df: pd.DataFrame()
    :type alpha: float

    :return: Tuple containing two pandas DataFrame objects
    """
    # Re-index to new range, so that we get the 9th month
    rng = pd.date_range(str(expo_df.index[0]), periods=9, freq='M').to_period('M')
    reindexed_expo_df = expo_df.reindex(rng)

    # Create a column of NaN values to the DataFrame
    reindexed_expo_df['ExpoSmooth'] = np.nan

    # Apply the expo smooth formula
    for i in range(len(reindexed_expo_df) - 1):
        if i == 0:
            reindexed_expo_df.ix[i, 'ExpoSmooth'] = reindexed_expo_df.ix[i, 'Open']
            reindexed_expo_df.ix[i + 1, 'ExpoSmooth'] = (alpha * reindexed_expo_df.ix[i, 'Open']) + \
                                                        ((1 - alpha) * reindexed_expo_df.ix[i, 'ExpoSmooth'])
        else:
            reindexed_expo_df.ix[i + 1, 'ExpoSmooth'] = (alpha * reindexed_expo_df.ix[i, 'Open']) + \
                                                        ((1 - alpha) * reindexed_expo_df.ix[i, 'ExpoSmooth'])

    return reindexed_expo_df
