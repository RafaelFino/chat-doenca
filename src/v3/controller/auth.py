from flask_restplus import Resource, Namespace, fields
from flask import request
from loguru import logger
from datetime import datetime
from base import Response, Services
from domain.message import Message

api = Namespace('Auth', description='Auth related operations')

authModel = api.model('AuthModel', {
    'password': fields.String
})

services = Services()

@api.route('/<id>')
class AuthController(Resource):
    @api.expect(authModel)
    def post(self, id: int):
        try:
            if id is None or len(id) == 0:
                return Response.create_error_response(400, 'Empty id')
                                    
            password = request.json.get('password')
                                   
            if password is None or len(password) == 0:
                return Response.create_error_response(400, 'Empty password')
            
            token = self.auth_service.login(id, password)
            return Response.create_response(201, 'User login', {'token': token})
                        
        except Exception as e:
            logger.error(f'Error to login user {id}: {e}')
            return Response.create_response(500, str(e))
        
    def delete(self, id: int):
        try:
            if id is None or len(id) == 0:
                return self.create_error_response(400, 'Empty id')
                                    
            if self.auth_service.logout(id):
                return Response.create_response(201, 'User logout', {'result': True})
            else:
                return Response.create_error_response(404, 'User not found')
                        
        except Exception as e:
            logger.error(f'Error to login user {id}: {e}')
            return Response.create_response(500, str(e))        
