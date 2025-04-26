from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Setup the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///connections.db'
db = SQLAlchemy(app)

# Database model
class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_lat = db.Column(db.Float, nullable=False)
    from_lng = db.Column(db.Float, nullable=False)
    to_lat = db.Column(db.Float, nullable=False)
    to_lng = db.Column(db.Float, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    print("Received data:", data)

    # Optional: Clear old connections first if you want
    Connection.query.delete()

    for conn in data:
        new_conn = Connection(
            from_lat=conn['from']['lat'],
            from_lng=conn['from']['lng'],
            to_lat=conn['to']['lat'],
            to_lng=conn['to']['lng']
        )
        db.session.add(new_conn)

    db.session.commit()

    return jsonify({"status": "success"})

@app.route('/connections', methods=['GET'])
def get_connections():
    all_connections = Connection.query.all()
    result = []
    for conn in all_connections:
        result.append({
            "from": {"lat": conn.from_lat, "lng": conn.from_lng},
            "to": {"lat": conn.to_lat, "lng": conn.to_lng}
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)