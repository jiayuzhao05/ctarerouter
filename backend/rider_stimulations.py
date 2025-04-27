import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from station import generate_graph
from datetime import datetime

RIDER_FILE = '/mnt/data/riders_simulation.csv'
LOCATION_FILE = '/mnt/data/locations.csv'
ERROR_LOG = '/mnt/data/rider_path_errors.csv'


def simulate_rider_paths(G, riders_df, station_name_to_id):
    rider_paths = []
    error_logs = []

    for idx, rider in riders_df.iterrows():
        try:
            source_id = station_name_to_id[rider['start_station']]
            target_id = station_name_to_id[rider['end_station']]
            path = nx.shortest_path(G, source=source_id, target=target_id)

            rider_paths.append({
                'rider_id': idx,
                'path': path,
                'departure_time': rider['departure_time']
            })
        except Exception as e:
            error_logs.append({
                'rider_id': idx,
                'start_station': rider['start_station'],
                'end_station': rider['end_station'],
                'error': str(e)
            })

    if error_logs:
        pd.DataFrame(error_logs).to_csv(ERROR_LOG, index=False)
        print(f"some riders cannot find paths {ERROR_LOG}")

    return rider_paths

def plot_paths(G, rider_paths):
    print("Plotting rider paths...")
    plt.figure(figsize=(14, 14))

   for path_info in rider_paths:
        path = path_info['path']
        departure_time = datetime.strptime(path_info['departure_time'], "%Y-%m-%d %H:%M:%S")
        hour = departure_time.hour

# different colors in different timeslots
        if 6 <= hour < 9:
            color = 'blue'
        elif 9 <= hour < 16:
            color = 'green'
        elif 16 <= hour < 19:
            color = 'orange'
        else:
            color = 'purple'

        lats = [G.nodes[n]['lat'] for n in path]
        lngs = [G.nodes[n]['lng'] for n in path]
        plt.plot(lngs, lats, alpha=0.3, color=color)

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Rider Simulated Paths (Color by Time Period)')
    plt.grid(True)
    plt.savefig('/mnt/data/rider_paths_plot_colored.png')
    plt.show()


def main():
    G = generate_graph()
    riders = pd.read_csv(RIDER_FILE)
    locations = pd.read_csv(LOCATION_FILE)

    # station_name -> station_id
    stations_latlng = pd.DataFrame.from_dict(G.nodes(data=True), orient='index')
    stations_latlng.reset_index(inplace=True)
    stations_latlng.rename(columns={'index': 'station_id'}, inplace=True)

    stations_latlng['lat'] = stations_latlng['lat'].round(4)
    stations_latlng['lng'] = stations_latlng['lng'].round(4)
    locations['lat'] = locations['lat'].round(4)
    locations['lng'] = locations['lng'].round(4)

    merged = pd.merge(
        stations_latlng,
        locations[['station_name', 'lat', 'lng']],
        on=['lat', 'lng'],
        how='left'
    )

    station_name_to_id = pd.Series(merged['station_id'].values, index=merged['station_name']).to_dict()

    rider_paths = simulate_rider_paths(G, riders, station_name_to_id)
    plot_paths(G, rider_paths)

if __name__ == "__main__":
    main()
