
from flask import Flask, request, jsonify, make_response

db = [{
    'id': 1,
    'name': 'John Doe',
    'email': 'john@exemplo.com'
}]

def init_app(app: Flask):

    @app.route('/health', methods=['GET'])
    def health():
        print('health check')
        return make_response(jsonify({'status': 'healthy'}), 200)


    # create user
    @app.route('/user', methods=['POST'])
    def create_user():
        try:
            data = request.get_json()
            new_user = {
                'id': len(db) + 1,
                'name': data['name'],
                'email': data['email']
            }
            db.append(new_user)
            return make_response(jsonify(new_user), 201)
        except Exception as e:
            return make_response(jsonify({'error creating user': str(e)}), 500)

    # get all users
    @app.route('/users', methods=['GET'])
    def get_users():
        try:
            return make_response(jsonify([user for user in db]), 200)
        except Exception as e:
            return make_response(jsonify({'error getting users': str(e)}), 500)

    # get user by id
    @app.route('/user/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        try:
            user = next((user for user in db if user['id'] == user_id), None)
            if user:
                return make_response(jsonify(user), 200)
            else:
                return make_response(jsonify({'error': 'User not found'}), 404)
        except Exception as e:
            return make_response(jsonify({'error getting user': str(e)}), 500)

    # update user by id
    @app.route('/user/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        print("update_user")
        try:
            user = next((user for user in db if user['id'] == user_id), None)
            if user:
                data = request.get_json()
                user['name'] = data['name']
                user['email'] = data['email']
                return make_response(jsonify(user), 200)
            else:
                return make_response(jsonify({'error': 'User not found'}), 404)
        except Exception as e:
            return make_response(jsonify({'error updating user': str(e)}), 500)

    # delete user by id
    @app.route('/user/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        try:
            user = next((user for user in db if user['id'] == user_id), None)
            if user:
                db.remove(user)
                return make_response(jsonify({'message': 'User deleted'}), 200)
            else:
                return make_response(jsonify({'error': 'User not found'}), 404)
        except Exception as e:
            return make_response(jsonify({'error deleting user': str(e)}), 500)