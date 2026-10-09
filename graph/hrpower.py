import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("dataset/allpower.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

df['hour'] = df['timestamp'].dt.hour
df['day'] = df['timestamp'].dt.day
df['month'] = df['timestamp'].dt.month
df['year'] = df['timestamp'].dt.year
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['weekday'] = df['timestamp'].dt.day_name()

buildings = [
    'Academic',
    'Boys_main',
    'Boys_backup',
    'Facilities',
    'Girls_main',
    'Girls_backup',
    'Lecture',
    'Library',
    'Mess'
]
hourly = df.groupby('hour')[buildings].mean()
hourly_total = hourly.sum(axis=1)

plt.figure(figsize=(10, 6))
plt.plot(hourly_total.index, hourly_total.values, marker='o')

plt.title('Average Power Consumption by Hour')
plt.xlabel('Hour of Day')
plt.ylabel('Average Power (W)')
plt.xticks(range(24))
plt.grid(True)
plt.tight_layout()
plt.show()