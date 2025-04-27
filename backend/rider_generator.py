import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta


TOTAL_RIDERS = 2664500
BATCH_SIZE = 100000
DATE = datetime.now().date()

# timeslots proportion
TIME_PERIODS = [
    ("06:00", "09:00", 0.35),
    ("09:00", "16:00", 0.30),
    ("16:00", "19:00", 0.25),
    ("19:00", "24:00", 0.10)
]

STATIONS_FILE = 'stations.csv'
OUTPUT_FILE = 'output.csv'



def generate_departure_time():
    period = random.choices(TIME_PERIODS, weights=[p[2] for p in TIME_PERIODS], k=1)[0]
    start_time = datetime.strptime(period[0], "%H:%M")
    end_time = datetime.strptime(period[1], "%H:%M")

    if period[1] == "24:00":
        end_time = datetime.strptime("23:59", "%H:%M")  

    time_diff = (end_time - start_time).seconds
    random_seconds = random.randint(0, time_diff)

    departure_datetime = datetime.combine(DATE, start_time.time()) + timedelta(seconds=random_seconds)
    return departure_datetime.strftime("%Y-%m-%d %H:%M:%S")


def generate_riders():
    print("read station ridership...")
    stations = pd.read_csv(STATIONS_FILE)
    ridership = pd.read_csv("CTA_Average_Rail_Station_Ridership_1999_2024.csv")

    station_names = stations['station_id'].tolist()
    weights = ridership['RIDERSHIP_ID'].tolist()
    weights = np.array(weights)
    weights = weights / weights.sum()

    total_batches = TOTAL_RIDERS // BATCH_SIZE

    first_batch = True

    for batch in range(total_batches + 1):
        batch_size = BATCH_SIZE if batch < total_batches else TOTAL_RIDERS % BATCH_SIZE
        if batch_size == 0:
            break

        riders = []

        for _ in range(batch_size):
            start_station = random.choices(station_names)[0]
            end_station = start_station

            while end_station == start_station:
                end_station = random.choice(station_names)

            departure_time = datetime.now()

            riders.append({
                'start_station': start_station,
                'end_station': end_station,
                'departure_time': departure_time
            })

        df_batch = pd.DataFrame(riders)

        if first_batch:
            df_batch.to_csv(OUTPUT_FILE, index=False, mode='w')
            first_batch = False
        else:
            df_batch.to_csv(OUTPUT_FILE, index=False, header=False, mode='a')

        print(f"Progress: {(batch + 1) * BATCH_SIZE}/{TOTAL_RIDERS} riders...")

    print(f"Riderdata generated, {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_riders()

