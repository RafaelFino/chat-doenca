from controller.base import Response, services
from flask import request
from flask_restx import Resource, Namespace, fields
from loguru import logger

api = Namespace('Auth', description='Auth related operations')

authModel = api.model('AuthModel', {
    'password': fields.String
})

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
            
            token = services.auth_service().login(id, password)

            if token is None:
                return Response.create_error_response(404, 'User not found')
            
            return Response.create_response(200, 'User login success', {'token': token})
                        
        except Exception as e:
            logger.error(f'Error to login user {id}: {e}')
            return Response.create_error_response(500, str(e))

    @api.doc(params={'Authorization': {'in': 'header', 'description': 'Authorization token'}})
    def delete(self, id: int):
        try:
            if id is None or len(id) == 0:
                return Response.create_error_response(400, 'Empty id')
                                    
            if services.auth_service().logout(id):
                return Response.create_response(201, 'User logout', {'result': True})
            else:
                return Response.create_error_response(404, 'User not logged')
                        
        except Exception as e:
            logger.error(f'Error to login user {id}: {e}')
            return Response.create_error_response(500, str(e))        
