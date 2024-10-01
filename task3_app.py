from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import pymysql
from datetime import datetime

pymysql.install_as_MySQLdb()

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:irrelevant1@127.0.0.1/fitness_center_db?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# Define Models
class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    join_date = db.Column(db.Date, nullable=False)

class WorkoutSessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    workout_type = db.Column(db.String(50), nullable=False)

# Member Schema
class MemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'join_date')

# Workout Session Schema
class WorkoutSessionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'member_id', 'date', 'duration', 'workout_type')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

# Member CRUD operations (from previous task)
# ... (keep the member CRUD operations as they were)

# Workout Session CRUD operations

# Schedule a new workout session
@app.route('/workout_sessions', methods=['POST'])
def add_workout_session():
    try:
        member_id = request.json['member_id']
        date = datetime.strptime(request.json['date'], '%Y-%m-%d').date()
        duration = request.json['duration']
        workout_type = request.json['workout_type']

        new_session = WorkoutSessions(member_id=member_id, date=date, duration=duration, workout_type=workout_type)

        db.session.add(new_session)
        db.session.commit()

        return workout_session_schema.jsonify(new_session), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get all workout sessions
@app.route('/workout_sessions', methods=['GET'])
def get_workout_sessions():
    all_sessions = WorkoutSessions.query.all()
    result = workout_sessions_schema.dump(all_sessions)
    return jsonify(result)

# Get a specific workout session
@app.route('/workout_sessions/<id>', methods=['GET'])
def get_workout_session(id):
    session = WorkoutSessions.query.get(id)
    if session:
        return workout_session_schema.jsonify(session)
    return jsonify({"message": "Workout session not found"}), 404

# Update a workout session
@app.route('/workout_sessions/<id>', methods=['PUT'])
def update_workout_session(id):
    session = WorkoutSessions.query.get(id)
    if not session:
        return jsonify({"message": "Workout session not found"}), 404

    try:
        session.member_id = request.json.get('member_id', session.member_id)
        if 'date' in request.json:
            session.date = datetime.strptime(request.json['date'], '%Y-%m-%d').date()
        session.duration = request.json.get('duration', session.duration)
        session.workout_type = request.json.get('workout_type', session.workout_type)

        db.session.commit()
        return workout_session_schema.jsonify(session)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete a workout session
@app.route('/workout_sessions/<id>', methods=['DELETE'])
def delete_workout_session(id):
    session = WorkoutSessions.query.get(id)
    if not session:
        return jsonify({"message": "Workout session not found"}), 404

    db.session.delete(session)
    db.session.commit()

    return jsonify({"message": "Workout session deleted successfully"})

# Get all workout sessions for a specific member
@app.route('/members/<member_id>/workout_sessions', methods=['GET'])
def get_member_workout_sessions(member_id):
    member = Members.query.get(member_id)
    if not member:
        return jsonify({"message": "Member not found"}), 404

    sessions = WorkoutSessions.query.filter_by(member_id=member_id).all()
    result = workout_sessions_schema.dump(sessions)
    return jsonify(result)

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
