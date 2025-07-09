import pandas as pd
from sqlalchemy import create_engine

# DB config - update if different
db_user = 'postgres'
db_password = '06152327'
db_host = 'localhost'
db_port = '5432'
db_name = 'securecheck'

# Create DB engine
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Load cleaned CSV
df = pd.read_csv('data/cleaned_stops.csv')

# Write to PostgreSQL table
df.to_sql('police_logs', engine, if_exists='replace', index=False)

print("✅ Data loaded into PostgreSQL table: police_logs")