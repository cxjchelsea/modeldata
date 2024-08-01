# _*_ coding: utf-8 _*_
# @File:    fenge_excel
# @Time:    2024/3/25 9:54
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1


import random
from datetime import datetime, timedelta
import pandas as pd


def generate_random_datetime():
    # Define the date range
    start_date = datetime(2023, 6, 1)
    end_date = datetime(2023, 12, 31)

    # Generate a random date within the specified range
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

    # Define the time ranges
    time_ranges = [
        (datetime.combine(random_date, datetime.strptime('08:00', '%H:%M').time()),
         datetime.combine(random_date, datetime.strptime('12:00', '%H:%M').time())),
        (datetime.combine(random_date, datetime.strptime('14:00', '%H:%M').time()),
         datetime.combine(random_date, datetime.strptime('17:00', '%H:%M').time()))
    ]

    # Choose a random time range
    start_time, end_time = random.choice(time_ranges)

    # Generate a random datetime within the chosen range
    random_datetime = start_time + timedelta(seconds=random.randint(0, int((end_time - start_time).total_seconds())))

    return random_datetime.strftime("%Y-%m-%d %H:%M:%S")


random_times = [generate_random_datetime() for _ in range(198)]

# Convert data to DataFrame
data = {'Generated Time': random_times}
df = pd.DataFrame(data)

# Write DataFrame to Excel file
df.to_excel('random_times.xlsx', index=False)

print("Excel file 'random_times.xlsx' has been created.")
