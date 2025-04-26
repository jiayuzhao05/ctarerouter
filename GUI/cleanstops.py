import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from app import db, Station  # import your app's db and Station model
import re

# Load your CSV
df = pd.read_csv('ctastops.csv')  # <-- change this to your CSV filename

# Example of your columns: STOP_ID, Location
print(df.head())

# Clean the Location field
def extract_lat_lng(location_str):
    # Expected format: "(lat, lng)"
    match = re.match(r'\(([^,]+), ([^,]+)\)', location_str)
    if match:
        lat, lng = match.groups()
        return float(lat), float(lng)
    else:
        return None, None

# Optional: Clear existing stations first
with db.session.begin():
    Station.query.delete()

# Insert cleaned data
with db.session.begin():
    for _, row in df.iterrows():
        stop_id = int(row['STOP_ID'])
        lat, lng = extract_lat_lng(row['Location'])

        if lat is not None and lng is not None:
            station = Station(
                station_id=stop_id,
                lat=lat,
                lng=lng
            )
            db.session.add(station)

print("✅ Stations loaded successfully into the database.")