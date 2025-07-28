from api import *
from extensions import api
# --- API Endpoints ---
api.add_resource(ApiSignup, '/api/signup')
api.add_resource(ApiLogin, '/api/login')
api.add_resource(ApiUsers, '/api/users','/api/users/<string:userId>')
api.add_resource(ApiLocation,'/api/location/<string:location>','/api/location')
api.add_resource(ApiByLocation, '/api/<string:decide>/<string:location>')
api.add_resource(ApiSlots,'/api/slots/<string:lotId>/<int:slotId>')
api.add_resource(ApiLots,'/api/lot','/api/lot/<string:lotId>')
api.add_resource(ApiGetDetails,'/api/gets/<int:OccOrNot>/<string:field>/<string:spec>') 
api.add_resource(ApiBookSlot, '/api/book') 
api.add_resource(ApiSendMail,'/api/sendMail')
api.add_resource(ApiCharts, '/api/slotStats/<string:choice>')