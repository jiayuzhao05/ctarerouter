import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from app import db, Station  # import your app's db and Station model
import sqlite3

# Load your CSV
df = pd.read_csv('GUI/ctastops.csv')  # <-- change this to your CSV filename

# subset only the stop name, line colors and location
df = df[['STATION_NAME','Location']]

# convert location to lat long
df[['lat', 'lng']] = df['Location'].str.extract(r'\(([-\d.]+),\s*([-\d.]+)\)').astype(float)
df.drop(columns='Location', inplace=True)

# Example of your columns: STOP_ID, Location
df = df.drop_duplicates(subset='STATION_NAME', keep='first').reset_index(drop=True)

# REPLACE 'STATION_NAME' with numbers
df['STATION_NAME'] = df.index

df.rename(columns={'STATION_NAME':'station_id'}, inplace=True)

# Connect to sqlite3 and upload dataframe to sqlite table
conn = sqlite3.connect('stations_routes.db')
df.to_sql('stations',conn,if_exists='replace',index=False)
conn.close()
