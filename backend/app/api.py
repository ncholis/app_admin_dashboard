from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.security.mongoengine.models import User
from flask import jsonify, request
from flask_appbuilder.api import BaseApi, expose, safe
from flask_appbuilder.security.decorators import has_access

class UserApi(BaseApi):
    resource_name = "user"

    @expose('/', methods=['GET'])
    @safe
    @has_access
    def get_users(self):
        users = User.objects()
        return jsonify([user.to_json() for user in users])

    @expose('/', methods=['POST'])
    @safe
    @has_access
    def add_user(self):
        data = request.json
        user = User(username=data['username'], email=data['email'],
                    first_name=['first_name'], last_name=['last_name'],
                    password=['password'], role='Public')
        user.save()
        return jsonify(user.to_json()), 201

    @expose('/<string:username>', methods=['PUT'])
    @safe
    @has_access
    def update_user(self, username):
        data = request.json
        user = User.objects(username=username).first()
        if user:
            user.update(**data)
            user.reload()
            return jsonify(user.to_json())
        return jsonify({'error': 'User not found'}), 404

    @expose('/<string:username>', methods=['DELETE'])
    @safe
    @has_access
    def delete_user(self, username):
        user = User.objects(username=username).first()
        if user:
            user.delete()
            return jsonify({'msg': 'User deleted'}), 200
        return jsonify({'error': 'User not found'}), 404