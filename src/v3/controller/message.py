from controller.base import Response, services
from domain.message import Message
from domain.token import LoginStatus, Token
from flask import request
from flask_restx import Resource, Namespace, fields
from loguru import logger
import json

api = Namespace('Message',description='Message related operations')

messageModel = api.model('MessageModel', {
    'text': fields.String
})

@api.route('/')
class MessageController(Resource):    
    @api.expect(messageModel)
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'Authorization token'}})
    def post(self):
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
                        
            text = request.json.get('text')

            if text is None or len(text) == 0:
                return Response.create_error_response(400, 'Empty text')
            
            user = services.user_service().get(user_id)
            
            if user is None:
                return Response.create_error_response(404, 'User not found')
                       
            msg = Message(user, text)
           
            msg.set_id(services.message_service().send(msg))
            return Response.create_response(201, 'Message sent', {'id': msg.get_id()})
                        
        except Exception as e:
            logger.error(f'Error sending message: {e}')
            return Response.create_error_response(500, str(e))
        
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'Authorization token'}})
    @api.param('last','Last message id', required=False)
    def get(self):
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
            
            last = request.args.get('last', default = 0, type = int)
            
            m = services.message_service().get_from_last(last)
            if m is None:
                return Response.create_error_response(404, 'Message not found')
            
            data = []

            for msg in m:
                data.append(msg.ToJson())
            
            return Response.create_response(200, 'Message loaded', { 'data': data} )
        
        except Exception as e:
            logger.error(f'Error getting message: {e}')
            return Response.create_error_response(500, str(e))
