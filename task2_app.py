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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:irrelevant1@127.0.0.1/fitness_center_db'
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

# Member Schema
class MemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'join_date')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

# Create a new member
@app.route('/members', methods=['POST'])
def add_member():
    try:
        name = request.json['name']
        email = request.json['email']
        join_date = datetime.strptime(request.json['join_date'], '%Y-%m-%d').date()

        new_member = Members(name=name, email=email, join_date=join_date)

        db.session.add(new_member)
        db.session.commit()

        return member_schema.jsonify(new_member), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get all members
@app.route('/members', methods=['GET'])
def get_members():
    all_members = Members.query.all()
    result = members_schema.dump(all_members)
    return jsonify(result)

# Get a specific member
@app.route('/members/<id>', methods=['GET'])
def get_member(id):
    member = Members.query.get(id)
    if member:
        return member_schema.jsonify(member)
    return jsonify({"message": "Member not found"}), 404

# Update a member
@app.route('/members/<id>', methods=['PUT'])
def update_member(id):
    member = Members.query.get(id)
    if not member:
        return jsonify({"message": "Member not found"}), 404

    try:
        member.name = request.json.get('name', member.name)
        member.email = request.json.get('email', member.email)
        if 'join_date' in request.json:
            member.join_date = datetime.strptime(request.json['join_date'], '%Y-%m-%d').date()

        db.session.commit()
        return member_schema.jsonify(member)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete a member
@app.route('/members/<id>', methods=['DELETE'])
def delete_member(id):
    member = Members.query.get(id)
    if not member:
        return jsonify({"message": "Member not found"}), 404

    db.session.delete(member)
    db.session.commit()

    return jsonify({"message": "Member deleted successfully"})

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)