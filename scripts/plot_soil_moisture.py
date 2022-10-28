import requests
import pandas as pd
import numpy as np

import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def fetch_data(date, am):
    r = requests.get(
        'https://api.tinybird.co/v0/pipes/soil_moisture_pipe.json',
        params={
            'date': date,
            'am': str(am),
            'token': {TOKEN},
        })
    return pd.DataFrame(r.json()['data'])

  
def world_map(df):
    fig, ax = plt.subplots(1, 1, figsize=(20, 8))
    sns.heatmap(df, 
        cmap='RdYlBu', 
        cbar=False, 
        xticklabels=False, 
        yticklabels=False)
    ax.tick_params(left=False, 
                bottom=False)
    return fig.show() 


def plot_data(date, am):
    df_plot = (pd.DataFrame(fetch_data(date,am)["columns"].tolist())).replace(0, 999999).astype(int)
    world_map(df_plot)

def main():
    date='2022-10-22'
    am=0
    print(date)
    plot_data(date, am)

    am=1
    print(date)
    plot_data(date, am)

    df_plot_am = pd.DataFrame(fetch_data(date, 0)["columns"].tolist())
    df_plot_pm = pd.DataFrame(fetch_data(date, 1)["columns"].tolist())
    df_plot = (pd.DataFrame(np.maximum(df_plot_am.to_numpy(), df_plot_pm.to_numpy()))).replace(0, 999999).astype(int)

    print(date)
    world_map(df_plot)

    new_date = str(pd.to_datetime(date) + datetime.timedelta(days=1))[:10]
    df_plot_next_1_am = pd.DataFrame(fetch_data(new_date, 0)["columns"].tolist())
    df_plot_next_1_pm = pd.DataFrame(fetch_data(new_date, 1)["columns"].tolist())

    new_date = str(pd.to_datetime(date) + datetime.timedelta(days=2))[:10]
    df_plot_next_2_am = pd.DataFrame(fetch_data(new_date, 0)["columns"].tolist())
    df_plot_next_2_pm = pd.DataFrame(fetch_data(new_date, 1)["columns"].tolist())

    new_date = str(pd.to_datetime(date) + datetime.timedelta(days=3))[:10]
    df_plot_next_3_am = pd.DataFrame(fetch_data(new_date, 0)["columns"].tolist())
    df_plot_next_3_pm = pd.DataFrame(fetch_data(new_date, 1)["columns"].tolist())

    new_date = str(pd.to_datetime(date) + datetime.timedelta(days=4))[:10]
    df_plot_next_4_am = pd.DataFrame(fetch_data(new_date, 0)["columns"].tolist())
    df_plot_next_4_pm = pd.DataFrame(fetch_data(new_date, 1)["columns"].tolist())

    df_plot = pd.DataFrame(np.maximum(df_plot_am.to_numpy(), df_plot_pm.to_numpy()))
    df_plot = pd.DataFrame(np.maximum(df_plot.to_numpy(), df_plot_next_1_am.to_numpy(), df_plot_next_1_pm.to_numpy()))
    df_plot = pd.DataFrame(np.maximum(df_plot.to_numpy(), df_plot_next_2_am.to_numpy(), df_plot_next_2_pm.to_numpy()))
    df_plot = pd.DataFrame(np.maximum(df_plot.to_numpy(), df_plot_next_3_am.to_numpy(), df_plot_next_3_pm.to_numpy()))
    df_plot = pd.DataFrame(np.maximum(df_plot.to_numpy(), df_plot_next_4_am.to_numpy(), df_plot_next_4_pm.to_numpy()))

    df_plot = df_plot.replace(0, 999999).astype(int)
    print(date,'-',new_date)
    world_map(df_plot)

if __name__ == '__main__':
    main()
