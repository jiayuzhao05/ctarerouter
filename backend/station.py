import networkx as nx
import geopandas as gpd
import duckdb
import pathlib


stations_location = pathlib.Path(__file__).parent.parent/"instance"/"stations_routes.db"


def generate_graph(): # call this function to generate the graph that has all stations
    
    stations_gdf,routes_gdf = read_db_input()
    G = graph_add_node(stations_gdf)
    graph_add_edge(G,routes_gdf)

    return G


def read_db_input():

    con = duckdb.connect(stations_location)  

    stations_gdf = gpd.GeoDataFrame(con.execute("SELECT * FROM stations").df())
    routes_gdf = gpd.GeoDataFrame(con.execute("SELECT * FROM routes;").df())

    return stations_gdf,routes_gdf


def graph_add_node(stations_gdf):
    G = nx.Graph()

    for index, row in stations_gdf.iterrows():
        station_name, station_lat, station_lng = row["station_id"], row["lat"],row["lng"]
        G.add_node(station_name,lat = station_lat, lng = station_lng)

    return G

def graph_add_edge(G, routes_gdf):
    for index, row in routes_gdf.iterrows():
        G.add_edge(row["s_id1"], row["s_id2"])



