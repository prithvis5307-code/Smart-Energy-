# ==========================================
# 1. IMPORTS
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# 2. LOAD DATA
# ==========================================

df = pd.read_csv("dataset/allpower.csv")

df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')


# ==========================================
# 3. DEFINE BUILDINGS
# ==========================================

# Actual column names in the dataset
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


# Friendly names for displaying results
building_names = {
    'Academic': 'Academic Building',
    'Boys_main': 'Boys Dormitory - Main',
    'Boys_backup': 'Boys Dormitory - UPS',
    'Facilities': 'Facilities',
    'Girls_main': 'Girls Dormitory - Main',
    'Girls_backup': 'Girls Dormitory - UPS',
    'Lecture': 'Lecture',
    'Library': 'Library',
    'Mess': 'Mess'
}


# ==========================================
# 4. TIME FEATURES
# ==========================================

df['hour'] = df['timestamp'].dt.hour
df['day'] = df['timestamp'].dt.day
df['month'] = df['timestamp'].dt.month
df['year'] = df['timestamp'].dt.year
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['weekday'] = df['timestamp'].dt.day_name()


# ==========================================
# 5. AVERAGE POWER BY BUILDING
# ==========================================

average_power = (
    df[buildings]
    .mean()
    .sort_values(ascending=False)
)

# Replace column names with friendly names for display
average_power.index = average_power.index.map(building_names)

print("\nAverage Power by Building:")
print(average_power)


# ==========================================
# 6. HOURLY ANALYSIS
# ==========================================

df['total_power'] = df[buildings].sum(
    axis=1,
    min_count=1
)

hourly_total = df.groupby('hour')['total_power'].mean()

print("\nHourly Average Power:")
print(hourly_total)


# ==========================================
# 7. PEAK AND LOWEST HOURS
# ==========================================

peak_hour = hourly_total.idxmax()
peak_power = hourly_total.max()

low_hour = hourly_total.idxmin()
low_power = hourly_total.min()

print("\nPeak Hour:", peak_hour)
print("Peak Power:", peak_power / 1000, "kW")

print("Lowest Hour:", low_hour)
print("Lowest Power:", low_power / 1000, "kW")


# ==========================================
# 8. DAILY ENERGY
# ==========================================

# Power is in Watts.
# 1 minute of power measurement:
# Energy (kWh) = Power(W) / 1000 / 60

df['energy_kwh'] = df['total_power'] / 1000 / 60

daily_energy = df.groupby(
    df['timestamp'].dt.date
)['energy_kwh'].sum()

print("\nAverage Daily Energy:", daily_energy.mean(), "kWh")
print("Maximum Daily Energy:", daily_energy.max(), "kWh")
print("Minimum Daily Energy:", daily_energy.min(), "kWh")


# ==========================================
# 9. HIGH-CONSUMPTION DAYS
# ==========================================

top_days = daily_energy.nlargest(10)

print("\nTop 10 High-Consumption Days:")
print(top_days)

top_10_avg = top_days.mean()

increase = (
    (top_10_avg - daily_energy.mean())
    / daily_energy.mean()
) * 100

print("\nAverage of Top 10 Days:", top_10_avg, "kWh")
print("Top 10 Days Above Average:", increase, "%")


# ==========================================
# 10. BUILDING CONTRIBUTION AT PEAK HOUR
# ==========================================

peak_buildings = (
    df[df['hour'] == peak_hour][buildings]
    .mean()
    .sort_values(ascending=False)
)

# Replace actual column names with friendly names
peak_buildings.index = peak_buildings.index.map(building_names)

print("\nBuilding Contribution at Peak Hour:")
print(peak_buildings)

# ==========================================
# 11. DAILY DATA COVERAGE
# ==========================================

# Count how many building measurements are available
# at each timestamp
df['valid_buildings'] = df[buildings].notna().sum(axis=1)

# Calculate average number of available building
# measurements for each day
daily_coverage = df.groupby(
    df['timestamp'].dt.date
)['valid_buildings'].mean()

print("\nDaily Data Coverage:")
print(daily_coverage.describe())


# Coverage of the top 10 high-consumption days
top_day_coverage = daily_coverage.loc[top_days.index]

print("\nCoverage of Top 10 High-Consumption Days:")
print(top_day_coverage)

# ==========================================
# 12. MONTHLY ENERGY ANALYSIS
# ==========================================

df['date'] = df['timestamp'].dt.date

# Daily energy is already calculated above.
# Convert the index to datetime so we can resample by month.

daily_energy.index = pd.to_datetime(daily_energy.index)

monthly_energy = daily_energy.resample('ME').sum()

print("\nMonthly Energy Consumption:")
print(monthly_energy)

print("\nTop 10 Months by Energy Consumption:")
print(monthly_energy.nlargest(10))


print("\nAverage Monthly Energy:", monthly_energy.mean(), "kWh")
print("Maximum Monthly Energy:", monthly_energy.max(), "kWh")
print("Minimum Monthly Energy:", monthly_energy.min(), "kWh")

# ==========================================
# 13. ANOMALY DETECTION - DAILY ENERGY
# ==========================================

Q1 = daily_energy.quantile(0.25)
Q3 = daily_energy.quantile(0.75)

IQR = Q3 - Q1

upper_limit = Q3 + 1.5 * IQR
lower_limit = Q1 - 1.5 * IQR

anomalies = daily_energy[
    (daily_energy > upper_limit) |
    (daily_energy < lower_limit)
]

print("\nAnomaly Detection:")
print("Q1:", Q1, "kWh")
print("Q3:", Q3, "kWh")
print("IQR:", IQR, "kWh")

print("\nUpper Anomaly Limit:", upper_limit, "kWh")
print("Lower Anomaly Limit:", lower_limit, "kWh")

print("\nNumber of Anomalous Days:", len(anomalies))

print("\nAnomalous Days:")
print(anomalies.sort_values(ascending=False).head(20))

# ==========================================
# 14. BUILDING CONTRIBUTION ON ANOMALOUS DAYS
# ==========================================

# Daily energy for each building
building_daily_energy = (
    df.groupby(df['timestamp'].dt.date)[buildings]
    .sum()
    / 1000
    / 60
)

# Convert index from Python date to datetime
building_daily_energy.index = pd.to_datetime(
    building_daily_energy.index
)

# Select only anomalous days
anomaly_building_energy = building_daily_energy[
    building_daily_energy.index.isin(anomalies.index)
]

# Average energy consumed by each building
average_anomaly_energy = (
    anomaly_building_energy
    .mean()
    .sort_values(ascending=False)
)

# Friendly building names
average_anomaly_energy.index = (
    average_anomaly_energy.index.map(building_names)
)

print("\nAverage Building Energy on Anomalous Days:")
print(average_anomaly_energy)

# ==========================================
# 15. NORMAL VS ANOMALOUS BUILDING ENERGY
# ==========================================

# Normal days
normal_building_energy = building_daily_energy[
    ~building_daily_energy.index.isin(anomalies.index)
]

# Average energy on normal days
average_normal_energy = (
    normal_building_energy
    .mean()
)

# Average energy on anomalous days
average_anomaly_energy = (
    anomaly_building_energy
    .mean()
)

# Percentage increase
percentage_increase = (
    (average_anomaly_energy - average_normal_energy)
    / average_normal_energy
) * 100

percentage_increase = percentage_increase.sort_values(
    ascending=False
)

percentage_increase.index = (
    percentage_increase.index.map(building_names)
)

print("\nBuilding Percentage Increase During Anomalous Days:")
print(percentage_increase)


# ==========================================
# 16. ADDITIONAL ENERGY DURING ANOMALOUS DAYS
# ==========================================

# Average energy on normal days
average_normal_energy = (
    normal_building_energy
    .mean()
)

# Average energy on anomalous days
average_anomaly_energy = (
    anomaly_building_energy
    .mean()
)

# Additional energy consumed during anomalous days
additional_energy = (
    average_anomaly_energy - average_normal_energy
)

# Sort from highest additional consumption
additional_energy = additional_energy.sort_values(
    ascending=False
)

# Friendly building names
additional_energy.index = (
    additional_energy.index.map(building_names)
)

print("\nAdditional Energy Consumption During Anomalous Days:")
print(additional_energy)

# ==========================================
# 17. HOURLY CONSUMPTION ON ANOMALOUS DAYS
# ==========================================

# Select rows belonging to anomalous days
anomaly_dates = anomalies.index.date

anomaly_data = df[
    df['timestamp'].dt.date.isin(anomaly_dates)
]

# Average hourly power during anomalous days
anomaly_hourly_power = (
    anomaly_data.groupby('hour')['total_power']
    .mean()
)

print("\nHourly Power During Anomalous Days:")
print(anomaly_hourly_power)

print(
    "\nPeak Hour During Anomalous Days:",
    anomaly_hourly_power.idxmax()
)

print(
    "Peak Power During Anomalous Days:",
    anomaly_hourly_power.max() / 1000,
    "kW"
)