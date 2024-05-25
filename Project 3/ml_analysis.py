import logging

import pandas as pd
import matplotlib.pyplot as plt
import os

def perform_time_series_analysis(df):
    event_counts = df['EventName'].value_counts()
    logging.debug(event_counts)
    return event_counts

def generate_time_series_chart(event_counts):
    plt.figure(figsize=(12, 10))
    event_counts.plot(kind='bar')
    plt.title('Event Occurrences')
    plt.xlabel('Event Name')
    plt.ylabel('Number of Occurrences')
    plt.grid(axis='y')

    chart_directory = './charts'
    if not os.path.exists(chart_directory):
        os.makedirs(chart_directory)

    chart_path = os.path.join(chart_directory, 'event_chart.png')
    plt.savefig(chart_path)
    plt.close()
    return chart_path

def perform_analysis_and_generate_chart():
    df = load_and_preprocess_data()
    event_counts = perform_time_series_analysis(df)
    chart_path = generate_time_series_chart(event_counts)
    return chart_path

def load_and_preprocess_data():
    data = []

    with open('request_log.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            user_id = parts[0].strip().split(': ')[1]
            event_name = parts[1].strip().split(': ')[1]
            status_code = int(parts[2].strip().split(': ')[1])

            data.append({'UserID': user_id, 'EventName': event_name, 'StatusCode': status_code})

    df = pd.DataFrame(data)

    return df

event_counts = load_and_preprocess_data()

if __name__ == "__main__":
    chart_path = perform_analysis_and_generate_chart()
