import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mysql.connector

def fetch_stock_data(database):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="whx051021",
        database=database
    )
    
    query = "SELECT day, open, close, high, low FROM `img_gl` ORDER BY day"
    data = pd.read_sql(query, connection)
    connection.close()
    
    data['day'] = pd.to_datetime(data['day'])
    
    return data

def plot_kline(db_name):
    data = fetch_stock_data(db_name)

    if data.empty:
        print("没有可用数据")
        return

    fig, ax = plt.subplots(figsize=(12, 6))

    previous_close = None

    for index, row in data.iterrows():
        color = 'green' if row['close'] >= row['open'] else 'red'
        ax.plot([row['day'], row['day']], [row['low'], row['high']], color='black')
        ax.add_patch(plt.Rectangle(
            (mdates.date2num(row['day']) - 0.2, min(row['open'], row['close'])),
            width=0.4,
            height=abs(row['open'] - row['close']),
            color=color
        ))

        if previous_close is not None:
            ax.plot([mdates.date2num(previous_day), mdates.date2num(row['day'])],
                    [previous_close, row['open']],
                    color='blue', linestyle='--')

        previous_day = row['day']
        previous_close = row['close']

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)

    ax.set_title('长城财富 K 线图')
    ax.set_xlabel('日期')
    ax.set_ylabel('价格')
    ax.grid(True)
    plt.tight_layout()
    plt.show()
