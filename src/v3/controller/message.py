from flask_restplus import Resource, Namespace, fields
from flask import request
from loguru import logger
from datetime import datetime
from base import Controller
from domain.message import Message

api = Namespace('Message',description='Message related operations')

messageModel = api.model('MessageModel', {
    'text': fields.String
})

@api.route('/')
class MessageController(Resource):    
    @api.expect(messageModel)
    @api.param('id','New message id')
    def send(self):
        try:
            user_id = self.auth(request)
            
            if user_id is None or len(user_id) == 0:
                return self.create_error_response(401, 'Unauthorized')
                        
            text = request.json.get('text')

            if text is None or len(text) == 0:
                return self.create_error_response(400, 'Empty text')
            
            user = self.user_service.get(id)            
            msg = Message(user, text)
            
            msg.set_id(self.message_service.send(msg))
            return self.create_response(201, 'Message sent', {'id': msg.get_id})
                        
        except Exception as e:
            logger.error(f'Error sending message: {e}')
            return self.create_response(500, str(e))
        
    def get(self):
        try:
            user_id = self.auth(request)
            
            if user_id is None or len(user_id) == 0:
                return self.create_error_response(401, 'Unauthorized')
            
            last = request.args.get('last')
            
            m = self.message_service.get_from_last(last)
            if m is None:
                return self.create_error_response(404, 'Message not found')
            
            return self.create_response(200, 'Message loaded', { 'data': m.ToJson()} )
        
        except Exception as e:
            logger.error(f'Error getting message: {e}')
            return self.create_response(500, str(e))
        
@api.route('/<id>')
class MessageController(Resource):    
    def get(self, id: int):
        try:
            user_id = self.auth(request)
            
            if user_id is None or len(user_id) == 0:
                return self.create_error_response(401, 'Unauthorized')
            
            if not id.isdigit():
                return self.create_error_response(400, 'Invalid message index')
            
            id = int(id)
            if id < 0:
                id = 0
            
            m = self.message_service.get(id)
            if m is None:
                return self.create_error_response(404, 'Message not found')
            
            return self.create_response(200, 'Message loaded', { 'data': m.ToJson()} )
        
        except Exception as e:
            logger.error(f'Error getting message: {e}')
            return self.create_response(500, str(e))