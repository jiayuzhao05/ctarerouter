from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Setup the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///connections.db'
db = SQLAlchemy(app)

# --- Database Models ---

class Station(db.Model):
    station_id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)

class Route(db.Model):
    route_id = db.Column(db.Integer, primary_key=True)
    station_from_id = db.Column(db.Integer, db.ForeignKey('station.station_id'), nullable=False)
    station_to_id = db.Column(db.Integer, db.ForeignKey('station.station_id'), nullable=False)

# --- Create Tables ---
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    print("Received data:", data)

    # Clear existing data (optional)
    Route.query.delete()
    Station.query.delete()
    db.session.commit()

    # In-memory lookup to avoid inserting duplicate stations
    station_lookup = {}
    station_counter = 1

    # First, go through all connections and add unique stations
    for conn in data:
        from_key = (conn['from']['lat'], conn['from']['lng'])
        to_key = (conn['to']['lat'], conn['to']['lng'])

        if from_key not in station_lookup:
            station = Station(station_id=station_counter, lat=from_key[0], lng=from_key[1])
            db.session.add(station)
            station_lookup[from_key] = station_counter
            station_counter += 1

        if to_key not in station_lookup:
            station = Station(station_id=station_counter, lat=to_key[0], lng=to_key[1])
            db.session.add(station)
            station_lookup[to_key] = station_counter
            station_counter += 1

    db.session.commit()

    # Now create routes using the station IDs
    for conn in data:
        from_key = (conn['from']['lat'], conn['from']['lng'])
        to_key = (conn['to']['lat'], conn['to']['lng'])

        route = Route(
            station_from_id=station_lookup[from_key],
            station_to_id=station_lookup[to_key]
        )
        db.session.add(route)

    db.session.commit()

    return jsonify({"status": "success"})

@app.route('/connections', methods=['GET'])
def get_connections():
    # Fetch routes and reconstruct connections
    routes = Route.query.all()
    connections = []

    for route in routes:
        from_station = Station.query.get(route.station_from_id)
        to_station = Station.query.get(route.station_to_id)

        connections.append({
            "from": {"lat": from_station.lat, "lng": from_station.lng},
            "to": {"lat": to_station.lat, "lng": to_station.lng}
        })

    return jsonify(connections)

if __name__ == '__main__':
    app.run(debug=True)