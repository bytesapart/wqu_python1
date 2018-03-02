import pandas as pd
from sklearn.linear_model import LinearRegression


def perform_linear_regression(data_df):
    """
    This function performs a Linear Regression and prints the correlation coefficient to indicate it's strength
    :param data_df: The Dataframe consisting of the Data
    :return: None
    """
    print('---------- Performing Linear Regression ----------')
    # Reshape the DataFrame
    data_df.reset_index(inplace=True, drop=True)
    X = pd.DataFrame(list(data_df.index))
    y = pd.DataFrame(list(data_df['Open']))

    model = LinearRegression()
    model.fit(X, y)

    X_predict = pd.DataFrame([9])
    y_predict = model.predict(X_predict)

    # Print the correlation coefficient
    print('The 9th Value for the series is: %s' % str(y_predict[0][0]))
    print('The Correlation Coefficient is: %s' % str(model.coef_[0][0]))

