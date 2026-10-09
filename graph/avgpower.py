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

hourly_count = df.groupby('hour')[buildings].count()

average_power = df[buildings].mean().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
average_power.plot(kind='bar')

plt.title('Average Power Consumption by Building')
plt.xlabel('Building')
plt.ylabel('Average Power (W)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()