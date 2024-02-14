from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    def json(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}

db.create_all()

@app.route('/health', methods=['GET'])
def health():
    return make_response(jsonify({'status': 'healthy'}), 200)


# create user
@app.route('/user', methods=['POST'])
def create_user():
    try:
      data = request.get_json()
      new_user = User(name=data['name'], email=data['email'])
      db.session.add(new_user)
      db.session.commit()
      return make_response(jsonify(new_user.json()), 201)
    except Exception as e:
        return make_response(jsonify({'error creating user': str(e)}), 400)

# get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify([user.json() for user in users]), 200)
    except Exception as e:
        return make_response(jsonify({'error getting users': str(e)}), 500)

# get user by id
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if user:
            return make_response(jsonify(user.json()), 200)
        else:
            return make_response(jsonify({'error': 'User not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'error getting user': str(e)}), 500)

# update user by id
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if user:
            data = request.get_json()
            user.name = data['name']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify(user.json()), 200)
        else:
            return make_response(jsonify({'error': 'User not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'error updating user': str(e)}), 500)

# delete user by id
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': 'User deleted'}), 200)
        else:
            return make_response(jsonify({'error': 'User not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'error deleting user': str(e)}), 500)