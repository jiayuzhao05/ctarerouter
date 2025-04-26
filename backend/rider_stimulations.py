import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from station import generate_graph


def load_data():
    print("Loading data...")
    riders = pd.read_csv('riders_simulation.csv')
    locations = pd.read_csv('locations.csv')
    return riders, locations


def create_station_mapping(G, locations):
    print("Creating station name to station ID mapping...")

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
    return station_name_to_id


def simulate_rider_paths(G, riders, station_name_to_id):
    print("Simulating rider paths...")
    rider_paths = []

    for idx, rider in riders.iterrows():
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
            print(f"Error finding path for rider {idx}: {e}")

    return rider_paths


def plot_paths(G, rider_paths):
    print("Plotting rider paths...")
    plt.figure(figsize=(12, 12))

    for path_info in rider_paths:
        path = path_info['path']
        lats = [G.nodes[n]['lat'] for n in path]
        lngs = [G.nodes[n]['lng'] for n in path]
        plt.plot(lngs, lats, alpha=0.3)

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Rider Simulated Paths')
    plt.grid(True)
    plt.savefig('rider_paths_plot.png')
    plt.show()


def main():
    G = generate_graph()
    riders, locations = load_data()
    station_name_to_id = create_station_mapping(G, locations)
    rider_paths = simulate_rider_paths(G, riders, station_name_to_id)
    plot_paths(G, rider_paths)


if __name__ == "__main__":
    main()
