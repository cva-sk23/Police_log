import pandas as pd
import os

#  Load dataset
data_path = os.path.join('data', 'traffic_stops.csv')
df = pd.read_csv(data_path)

#  Drop columns that are completely empty
df.dropna(axis=1, how='all', inplace=True)

#  Fill missing values
df['driver_age'] = df['driver_age'].fillna(df['driver_age'].median())
df['driver_gender'] = df['driver_gender'].fillna('Unknown')
df['driver_race'] = df['driver_race'].fillna('Unknown')
df['violation'] = df['violation'].fillna('Unknown')
df['search_conducted'] = df['search_conducted'].fillna(False)
df['search_type'] = df['search_type'].fillna('None')
df['stop_outcome'] = df['stop_outcome'].fillna('Unknown')
df['is_arrested'] = df['is_arrested'].fillna(False)
df['stop_duration'] = df['stop_duration'].fillna('Unknown')
df['drugs_related_stop'] = df['drugs_related_stop'].fillna(False)
#  Format date and time
df['stop_date'] = pd.to_datetime(df['stop_date'], errors='coerce').dt.date
df['stop_time'] = pd.to_datetime(df['stop_time'], errors='coerce').dt.time
#  Drop rows with invalid datetime
df.dropna(subset=['stop_date', 'stop_time'], inplace=True)
#  Save cleaned file
output_path = os.path.join('data', 'cleaned_stops.csv')
df.to_csv(output_path, index=False)
print(" Data cleaned and saved to /data/cleaned_stops.csv")