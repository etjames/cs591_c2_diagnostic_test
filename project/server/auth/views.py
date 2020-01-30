# project/server/auth/views.py

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import User

auth_blueprint = Blueprint('auth', __name__)

class UserListAPI(MethodView):
    """
    User List Resource
    """

    def get(self):

        string = "users:"
            
        q = User.query.all()
        for users in q:
            string += " "
            string += (users.email)

        return make_response(string), 201

class HomepageAPI(MethodView):
    """
    User List Resource
    """

    def get(self):

        string = "Hello! Welcome to CS591 Assignment 1."
        return make_response(string), 201


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """


    def get(self):
    	responseObject = {
    		'status': 'success',
    		'message': 'Request successful but please send an HTTP POST request to register the user.'
    	}
    	return make_response(jsonify(responseObject)), 201

    def post(self):
        # get the post data
        post_data = request.get_json(); print(request)
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )

                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202


# define the API resources
registration_view = RegisterAPI.as_view('register_api')
user_list_view = UserListAPI.as_view('user_list_api')
homepage_view = HomepageAPI.as_view('homepage_view')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST', 'GET']

)

auth_blueprint.add_url_rule(
    '/users/index',
    view_func=user_list_view,
    methods=['GET']

)

auth_blueprint.add_url_rule(
    '/',
    view_func=homepage_view,
    methods=['GET']

)
