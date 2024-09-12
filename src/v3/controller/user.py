from controller.base import Response, services
from flask import request
from flask_restx import Resource, Namespace, fields
from loguru import logger
from domain.token import LoginStatus, Token

api = Namespace('User',description='User related operations')

userModel = api.model('UserModel', {
    'name': fields.String,
    'password': fields.String
})

updateModel = api.model('UpdateModel', {
    'enable': fields.Boolean
})

@api.route('/')
class UserController(Resource):
    @api.expect(userModel)
    def post(self):
        try:                       
            name = request.json.get('name')
            password = request.json.get('password')
            
            if name is None or len(name) == 0:
                return Response.create_error_response(400, 'Empty name')
                       
            if password is None or len(password) == 0:
                return Response.create_error_response(400, 'Empty password')
            
            id = services.user_service().create(name, password)
            return Response.create_response(201, 'User created', {'id': id})
                        
        except Exception as e:
            logger.error(f'Error creating user: {e}')
            return Response.create_error_response(500, str(e))

@api.route('/<id>')
@api.doc(params={'Authorization': {'in': 'header', 'description': 'Authorization token'}})
class UserIdController(Resource):        
    def get(self, id):
        try:
            token = services.auth(request)

            if token is None:
                return Response.create_error_response(401, 'Unauthorized', 'User or token not found')
            
            if token.status is LoginStatus.REJECTED:
                return Response.create_error_response(403, 'Forbidden', 'Invalid token')
            
            if token.status is LoginStatus.EXPIRED:
                return Response.create_error_response(401, 'Unauthorized', "Token expired")
            
            if token.user is None:
                return Response.create_error_response(401, 'Unauthorized', 'User not found')

            user_id = token.get_user_id()
            
            if user_id is None:
                return Response.create_error_response(401, 'Unauthorized')
            
            user = services.user_service().get(id)
            if user is None:
                return Response.create_error_response(404, 'User not found')
            
            return Response.create_response(200, 'User loaded', { 'user': user.ToJson()} )
        
        except Exception as e:
            logger.error(f'Error getting user: {e}')
            return Response.create_error_response(500, str(e))
        
    @api.expect(updateModel)
    def put(self, id):
        try:
            token = services.auth(request)

            if token is None:
                return Response.create_error_response(401, 'Unauthorized', 'User or token not found')
            
            if token.status is LoginStatus.REJECTED:
                return Response.create_error_response(403, 'Forbidden', 'Invalid token')
            
            if token.status is LoginStatus.EXPIRED:
                return Response.create_error_response(401, 'Unauthorized', "Token expired")
            
            if token.user is None:
                return Response.create_error_response(401, 'Unauthorized', 'User not found')

            user_id = token.get_user_id()
            
            if user_id is None:
                return Response.create_error_response(401, 'Unauthorized')
            
            enable = request.json.get('enable')
            if enable is None:
                return Response.create_error_response(400, 'Empty enable field')
            
            if not services.user_service().put(id, enable):                
                return Response.create_error_response(500, 'Error updating user')
            
            return Response.create_response(200, 'User updated')
        
        except Exception as e:
            logger.error(f'Error updating user: {e}')
            return Response.create_error_response(500, str(e))
        
