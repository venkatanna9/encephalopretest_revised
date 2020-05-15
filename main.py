# Encephalo Investments Coding Pre-Test - Revised April 2020

import pandas as pd
import numpy as np
import math


def cleanse_data(df):
    # Your task here is to remove data from any ticker that isn't XXY, sort chronologically and return a dataframe
    # whose only column is 'Adj Close'
    dfclean = df[df.Ticker == 'XXY']
    dfclean = dfclean.sort_values(by='Date')
    adj_close = dfclean.drop(['Date','Ticker'], axis=1)
    return adj_close


def mc_sim(sims, days, df):
    # The code for a crude monte carlo simulation is given below. Your job is to extract the mean expected price
    # on the last day, as well as the 95% confidence interval.
    # Note that the z-score for a 95% confidence interval is 1.960
    returns = df.pct_change()
    last_price = float(df.iloc[-1])

    simulation_df = pd.DataFrame()

    for x in range(sims):
        count = 0
        daily_vol = returns.std()

        price_series = []

        price = last_price * (1 + np.random.normal(0, daily_vol))
        price_series.append(price)

        for y in range(days):
            price = price_series[count] * (1 + np.random.normal(0, daily_vol))
            price_series.append(price)
            count += 1

        simulation_df[x] = price_series

    # FILL OUT THE REST OF THE CODE. The above code has given you 'sims' of simulations run 'days' days into the future.
    # Your task is to return the expected price on the last day +/- the 95% confidence interval.
    average = np.mean(simulation_df.iloc[-1])
    std = np.std(simulation_df.iloc[-1])
    above = 1.96 * std + average
    under = -1.96 * std + average
    return above, under

def main():
    filename = '20192020histdata.csv'
    rawdata = pd.read_csv(filename)
    cleansed = cleanse_data(rawdata)
    simnum = 100  # change this number to one that you deem appropriate
    days = 25
    above = mc_sim(simnum, days, cleansed)
    under = mc_sim(simnum, days, cleansed)
    return above, under


if __name__ == '__main__':
    main()
    above, under = main()
    print("The expected price on the last day + 95% confidence interval is: ", above)
    print("The expected price on the last day - 95% confidence interval is: ", under)
