# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas",
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///

## Bitcoin Monte Carlo ##
## 27 August 2024      ##


import pandas as pd
import numpy as np
from scipy.stats import genhyperbolic
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib
matplotlib.use("Agg")


df_csv  = pd.read_csv("btc_price_data.csv")
last_date = df_csv["Date"].iloc[-1] # or "2023-07-20"
df = df_csv[df_csv["Date"] < last_date].copy()
n_sims = 1000
n_days = 365
last_price = df['Close'].iloc[-1]


def add_returns_columns(df):
    df['log_return'] = np.log(df['Close'] / df['Close'].shift(1))
    return df


def generate_monte_carlo_simulations(df, n_sims, n_days):
    df = df['log_return'].dropna()
    params = genhyperbolic.fit(df)
    simulation_returns = genhyperbolic.rvs(*params, size=(n_sims, n_days))
    return simulation_returns


def project_future_prices(last_price, simulation_returns):
    cumulative_log_returns = np.cumsum(simulation_returns, axis=1)
    relative_prices = np.exp(cumulative_log_returns)
    simulation_prices = last_price * relative_prices
    return simulation_prices


def log_format(y, pos):
    return f'${int(y):,}'


def format_text(num):
    return f'${int(num):,}'


def graph_simulations(simulation_prices, start_price):
    fig, ax = plt.subplots(figsize=(8,6))
    for simulation in simulation_prices:
    	ax.plot(simulation, alpha=0.075)

    ax.set_yscale('log')
    ax.yaxis.set_major_formatter(FuncFormatter(log_format))
    
    avg_prices = simulation_prices.mean(axis=0)
    med_prices = np.median(simulation_prices, axis=0)
    ax.plot(avg_prices, color='orange', label='Average')
    ax.plot(med_prices, color='blue', label='Median')
    avg_last_price = format_text(avg_prices[-1])
    med_last_price = format_text(med_prices[-1])
    
    ax.set_title("Bitcoin 1YR Monte Carlo Simulations")
    ax.text(369, avg_prices[-1], format_text(avg_prices[-1]))
    ax.text(369, med_prices[-1]-3000, format_text(med_prices[-1]))
    ax.text(0, last_price+10000, format_text(start_price))
    
    for spine in ax.spines.values():
        spine.set_color("#bababa")
    
    ax.legend()
    fig.savefig("all_simulations_chart.png")

def main():
    simulation_returns = generate_monte_carlo_simulations(add_returns_columns(df), n_sims, n_days)
    simulation_prices = project_future_prices(last_price, simulation_returns)
    graph_simulations(simulation_prices, last_price)


if __name__ == '__main__':
    main()
