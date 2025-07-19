import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
np.float = float
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
data_file = "fcc-forum-pageviews.csv"
df = pd.read_csv(data_file, index_col="date")
df.index = pd.to_datetime(df.index)

# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(0.025)) 
    & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    sns.lineplot(data=df.copy(), x=df.index, y="value", ax=ax)
    ax.set_xlabel('Date')
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    full_mon_order = ["January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December"]
    df_bar = df.copy()
    df_bar['Years'] = df_bar.index.year
    df_bar['Month'] = df_bar.index.month_name()
    df_bar['Month'] = pd.Categorical(df_bar["Month"], categories=full_mon_order, ordered=True)
    df_bar_grouped = df_bar.groupby(["Years", "Month"], sort=False)['value'].mean().round(2)
    df_bar_grouped = df_bar_grouped.reset_index()
    df_bar_grouped.rename(columns= {
        "value": "Average Page Views"
        }, inplace=True)
    
    # Draw bar plot
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(data=df_bar_grouped, x="Years", y="Average Page Views", 
    hue="Month", palette="tab20",ax=ax)
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    sns.boxplot(data=df_box, x = "year", y="value", ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_ylabel("Page Views")
    axes[0].set_xlabel("Year")

    mon_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(data=df_box, x = "month", y="value", order=mon_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_ylabel("Page Views")
    axes[1].set_xlabel("Month")


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
