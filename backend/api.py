from flask_restful import Resource
import json
from flask import request,jsonify
from datetime import datetime
from flask_jwt_extended import create_access_token, jwt_required,get_jwt_identity
from flask import send_from_directory

from extensions import *
from model import *
from func import gen_user_id,gen_lot_id,send_mail

# --- Signup Route ---
class ApiSignup(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            return {'message': 'Missing fields'}, 400
        if User.query.filter_by(email=email).first():
            return {'message': 'Email already exists'}, 409

        new_user = User(userId=gen_user_id(), name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created'}, 201

# --- Login Route ---
class ApiLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email, password=password).first()
        if not user:
            return {'message': 'Invalid email or password'}, 401

        access_token = create_access_token(identity=user.email)
        is_admin = user.email == 'admin@example.com'

        return {
            'access_token': access_token,
            'user': {
                'userId': user.userId,
                'name': user.name,
                'email': user.email,
                'isAdmin': is_admin
            }
        }, 200

# --- Protected Dashboard Route ---
class ApiUsers(Resource):
    @jwt_required()
    def get(self,userId=None):
        
        if not userId:
            current_user_email = get_jwt_identity()
            user = User.query.filter_by(email=current_user_email).first()
            userId=user.userId
            if not user:
                return {'message': 'User not found'}, 404
            if user.email == 'admin@example.com':
                cachedUsers= red.get('user_list')
                if cachedUsers:
                    print("Cache hit for user list")
                    return jsonify(json.loads(cachedUsers))
                users = User.query.all()
                user_list = [{
                    'userId': user.userId,
                    'name': user.name,
                    'email': user.email,
                    'address':user.address
                } for user in users if user.userId!=100000]
                red.set('user_list', json.dumps(user_list), ex=10)  # Cache for 1 hour
                return jsonify(user_list)
            else:
                return {"message":f"Welcome to the dashboard,{user.name}"}, 200
        else :
            userData=User.query.filter_by(userId=userId).first()
            userDict={"userId":userData.userId,"name":userData.name,"email":userData.email,"address":userData.address}
            return jsonify(userDict)
        
    @jwt_required()
    def put(self):
        data=request.get_json()
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        address=data.get("address")
        name=data.get("name")
        if not address or not name:
            return {"message":"Missing fields, fields required"},200
        user.name=name
        user.address=address
        db.session.commit()
        return {"message":"The profile updates successfully"},200

class ApiLocation(Resource):
    def get(self,location=None):
        if not location:
            cachedLocations= red.get('location_list')
            if cachedLocations:
                print("Cache hit for location list")
                return jsonify(json.loads(cachedLocations))
            locations=Locations.query.all()
            data=[loc.location.strip() for loc in locations]
            print(data)
            newData=list(set(data))  # Remove duplicates
            location_list={"location": newData }
            red.set('location_list', json.dumps(location_list), ex=100)  
            return jsonify(location_list)
        else:
            cachedLocation=red.get(f'location_{location}')
            if cachedLocation:
                print("Cache hit for location details")
                return jsonify(json.loads(cachedLocation))
            location_entry = Locations.query.filter_by(location=location).first()
            locDict={}
            if location_entry:
                locDict['location'] = location_entry.location
                locDict['address'] = location_entry.address
                locDict['pincode'] = location_entry.pincode
            red.set(f'location_{location}', json.dumps(locDict), ex=10) 
            return jsonify(locDict)

    def post(self, location=None):
        if location:
            return {'message': 'URL does not accept location parameter'}, 400
        data=request.get_json()
        location=data.get('location')
        #lotId=gen_lot_id()
        address=data.get('address')
        pincode=data.get('pincode')
        print(address,pincode,location)
        #maxSlots=data.get('maxSlots')
        #price=data.get('price')
        if not location or not address or not pincode:
            return {'message': 'Missing fields'}, 400
        if Locations.query.filter_by(location=location).first():
            return {'message': 'Location already exists'}, 409
        new_location = Locations(location=location, address=address,pincode=pincode)
        db.session.add(new_location)
        db.session.commit()
        return {'message': 'Location added successfully'}, 201
    
    @jwt_required()
    def delete(self, location=None):
        if not location:
            return {'message': 'Location parameter is required'}, 400
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.email != 'admin@example.com':
            return {'message': 'Unauthorized'}, 403
        location_entry = Locations.query.filter_by(location=location).first()
        print(location_entry)
        if location_entry:
            location= location_entry.location
            lots = Lots.query.filter_by(location=location).all()
            for lot in lots:
                occupied_slots = OccupiedSlot.query.filter_by(lotId=lot.lotId).all()
                for occupied in occupied_slots:
                    db.session.delete(occupied)
                slots = Slots.query.filter_by(lotId=lot.lotId).all()
                for slot in slots:
                    db.session.delete(slot)
                db.session.delete(lot)
            db.session.delete(location_entry)
            db.session.commit()
            return {'message': 'Location deleted successfully'}, 200
        else:
            return {'message': 'Location not found'}, 404
    
    def put(self, location=None):
        if not location:
            return {'message': 'Location parameter is required'}, 400
        #adminAccess()
        data = request.get_json()
        new_location = data.get('location')
        new_address = data.get('address')
        new_pincode = data.get('pincode')

        if not new_location and not new_address and not new_pincode:
            return {'message': 'No fields to update'}, 400
        if new_location:
            lot_entry= Lots.query.filter_by(location=location).all()
            for lot in lot_entry:
                lot.location = new_location

        location_entry = Locations.query.filter_by(location=location).first()
        if not location_entry:
            return {'message': 'Location not found'}, 404

        if new_location:
            existing = Locations.query.filter_by(location=new_location).first()
            if existing and existing.id != location_entry.id:
                return {'message': 'New location already exists'}, 409
            location_entry.location = new_location

        if new_address:
            location_entry.address = new_address

        if new_pincode:
            location_entry.pincode = new_pincode

        try:
            db.session.commit()
            return {'message': 'Location updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Update failed', 'error': str(e)}, 500

class ApiByLocation(Resource):
    def get(self, location, decide):
        if decide == "slots":
            if location=="all":
                entry = Lots.query.all()
            else:
                entry = Lots.query.filter_by(location=location).all()
            lotIds = [ent.lotId for ent in entry]
            lotSlots = {}
            lotDetails = {}
            
            for lot in entry:
                slots = Slots.query.filter_by(lotId=lot.lotId).all()
                notOccupiedNo = Slots.query.filter_by(lotId=lot.lotId, isOccupied=False).count()
                slotsList = [(slot.slotId, slot.isOccupied) for slot in slots]
                lotSlots[lot.lotId] = slotsList
                lotDetails[lot.lotId] = [notOccupiedNo, lot.maxSlots, lot.price]
            print(lotSlots, lotDetails  )
            return jsonify([lotSlots, lotDetails])

class ApiSlots(Resource):
    def get(self,slotId=None,lotId=None):
        if not slotId or not lotId:
            return {'message': 'SlotId and LotId parameters are required'}, 400
        slots = Slots.query.filter_by(lotId=lotId, slotId=slotId).first()
        if not slots:
            return {'message': 'Slot not found'}, 404
        isOccupied = slots.isOccupied
        if isOccupied:
            occupied_slot = OccupiedSlot.query.filter_by(slotId=slotId, lotId=lotId).first()
            return {
            'slotId': slots.slotId,
            'lotId': slots.lotId,
            'isOccupied': isOccupied,
            'userId': occupied_slot.userId if occupied_slot else None,
            'startTime': str(occupied_slot.startTime) if occupied_slot else None,
            'endTime': str(occupied_slot.endTime) if occupied_slot else None,
            'vehicleNo': occupied_slot.vehicleNo if occupied_slot else None,
            'price': occupied_slot.price  if occupied_slot else None
        }, 200
        if isOccupied and not occupied_slot:
            return {'message': 'Slot is occupied but no details found'},200
        return {
            'slotId': slots.slotId,
            'lotId': slots.lotId,
            'isOccupied': isOccupied,
            'userId': None,
            'startTime': None,
            'endTime': None,
            'vehicleNo': None,
            'price': None
        }, 200
    
    @jwt_required()
    def delete(self,slotId=None, lotId=None):
        if not slotId or not lotId:
            return {'message': 'SlotId and LotId parameters are required'}, 400

        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()

        if not user or user.email != 'admin@example.com':
            return {'message': 'Unauthorized'}, 403

        try:
            slotId = int(slotId)
        except ValueError:
            return {'message': 'Invalid SlotId'}, 400

        slot = Slots.query.filter_by(lotId=lotId, slotId=slotId).first()
        if not slot:
            return {'message': 'Slot not found'}, 404

        db.session.delete(slot)

        slots_to_update = Slots.query.filter(
            Slots.lotId == lotId,
            Slots.slotId > slotId
        ).order_by(Slots.slotId.asc()).all()

        for s in slots_to_update:
            s.slotId -= 1

        db.session.commit()
        return {'message': f'Slot {slotId} deleted and slots renumbered'}, 200
 
class ApiLots(Resource):
    def get(self,lotId=None):
        if not lotId:
            lots=Lots.query.all()
            lotList = [{
                    'lotId': lot.lotId,
                    'location': lot.location,
                    'maxSlots': lot.maxSlots,
                    'price': lot.price
                } for lot in lots]
            return jsonify({"lotList": lotList})
        else:
            lot = Lots.query.filter_by(lotId=lotId).first()
            if not lot:
                return {'message': 'Lot not found'}, 404
            return {
                'lotId': lot.lotId,
                'location': lot.location,
                'maxSlots': lot.maxSlots,
                'price': lot.price
            }, 200
        
    @jwt_required()
    def post(self,lotId=None):
        if lotId:
            return {'message': 'URL does not accept lotId parameter'}, 400
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.email != 'admin@example.com':
            return {'message': 'Unauthorized'}, 403
        data = request.get_json()
        lotId = gen_lot_id()
        maxSlots = int(data.get('maxSlots'))
        location = data.get('location')
        price = int(data.get('price'))
        print(lotId, maxSlots, price)
        if not maxSlots or not price:
            return {'message': 'Missing fields'}, 400
        addLot = Lots(lotId=lotId, location=location, maxSlots=maxSlots, price=price)
        for i in range(1,maxSlots+1):
            addSlot = Slots(slotId=i, lotId=lotId, isOccupied=False)
            db.session.add(addSlot)
        db.session.add(addLot)
        db.session.commit()
        return {'message': 'Lot added successfully',"lotId":lotId}, 201
    
    @jwt_required()
    def put(self, lotId=None):
        if not lotId:
            return {'message': 'LotId parameter is required'}, 400
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.email != 'admin@example.com':
            return {'message': 'Unauthorized'}, 403
        data = request.get_json()
        new_location = data.get('location')
        new_max_slots = data.get('maxSlots')
        new_price = data.get('price')
        print(lotId, new_location, new_max_slots, new_price)
        lot = Lots.query.filter_by(lotId=lotId).first()
        if not lot:
            return {'message': 'Lot not found'}, 200
        existing = Lots.query.filter_by(location=new_location).first()
        new_lot=Lots.query.filter_by(lotId=lotId).first()
        if new_price:
            new_lot.price = new_price
        if new_location:
            if existing:
                new_lot.location = new_location
            else:
                return {'message': 'Location does not exist'}, 200
        if new_max_slots:
            try:
                new_max_slots = int(new_max_slots)
                if new_max_slots < 0:
                    return {'message': 'Max slots cannot be negative'}, 400
                new_lot.maxSlots = new_max_slots
                current_slots = Slots.query.filter_by(lotId=lotId).count()
                if current_slots < new_max_slots:
                    for i in range(current_slots + 1, new_max_slots + 1):
                        addSlot = Slots(slotId=i, lotId=lotId, isOccupied=False)
                        db.session.add(addSlot)
                elif current_slots > new_max_slots:
                    for i in range(new_max_slots + 1, current_slots + 1):
                        slot_to_delete = Slots.query.filter_by(slotId=i, lotId=lotId).first()
                        if slot_to_delete:
                            db.session.delete(slot_to_delete)
            except ValueError:
                return {'message': 'Invalid max slots value'}, 400
        try:
            db.session.commit()
            return {'message': 'Lot updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Update failed', 'error': str(e)}, 500
        
    @jwt_required()
    def delete(self, lotId=None):
        if not lotId:
            return {'message': 'LotId parameter is required'}, 400
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.email != 'admin@example.com':
            return {'message': 'Unauthorized'}, 403
        lot = Lots.query.filter_by(lotId=lotId).first()
        if not lot:
            return {'message': 'Lot not found'}, 404
        occupied_slots = OccupiedSlot.query.filter_by(lotId=lotId).all()
        if occupied_slots:
            return {'message': 'Cannot delete lot with occupied slots'}, 200
        slots = Slots.query.filter_by(lotId=lotId).all()
        for slot in slots:
            db.session.delete(slot)
        db.session.delete(lot)
        db.session.commit()
        return {'message': 'Lot deleted successfully'}, 200

class ApiGetDetails(Resource):
    def get(self,OccOrNot=2,field=None,spec=None):
        detailsList=[]
        if not field:
            return {'message': 'Field parameter is required'}, 400
        if field=="location":
            if spec=="all":
                details=Lots.query.all()
                for detail in details:
                    slots=Slots.query.filter_by(lotId=detail.lotId).all()
                    for slot in slots:
                        if OccOrNot==2 :
                            detailsList.append({"lotId":detail.lotId,"location":detail.location,"slotId":slot.slotId,"isOccupied":slot.isOccupied})
                        elif OccOrNot==0 and slot.isOccupied== False:
                            detailsList.append({"lotId":detail.lotId,"location":detail.location,"slotId":slot.slotId,"isOccupied":slot.isOccupied})
                        elif OccOrNot==1 and slot.isOccupied== True:
                            detailsList.append({"lotId":detail.lotId,"location":detail.location,"slotId":slot.slotId,"isOccupied":slot.isOccupied})
                return jsonify(detailsList)
            else:
                details=Lots.query.filter_by(location=spec).all()
                for detail in details:
                    slots=Slots.query.filter_by(lotId=detail.lotId).all()
                    for slot in slots:
                        if OccOrNot==2 :
                            detailsList.append({"lotId":detail.lotId,"location":detail.location,"slotId":slot.slotId,"isOccupied":slot.isOccupied})
                        elif OccOrNot==0 and slot.isOccupied== False:
                            detailsList.append({"lotId":detail.lotId,"location":detail.location,"slotId":slot.slotId,"isOccupied":slot.isOccupied})
                        elif OccOrNot==1 and slot.isOccupied== True:
                            detailsList.append({"lotId":detail.lotId,"location":detail.location,"slotId":slot.slotId,"isOccupied":slot.isOccupied})
                #print(detailsList)
                return jsonify(detailsList)
        elif field=="lotId":
            if not spec:
                return {'message': 'Spec parameter is required'}, 400
            lot = Lots.query.filter_by(lotId=spec).first()
            if not lot:
                return {'message': 'Lot not found'}, 404
            slots = Slots.query.filter_by(lotId=spec).all()
            for slot in slots:
                if OccOrNot == 2:
                    detailsList.append({"lotId": lot.lotId, "location": lot.location, "slotId": slot.slotId, "isOccupied": slot.isOccupied})
                elif OccOrNot == 0 and slot.isOccupied == False:
                    detailsList.append({"lotId": lot.lotId, "location": lot.location, "slotId": slot.slotId, "isOccupied": slot.isOccupied})
                elif OccOrNot == 1 and slot.isOccupied == True:
                    detailsList.append({"lotId": lot.lotId, "location": lot.location, "slotId": slot.slotId, "isOccupied": slot.isOccupied})
            return jsonify(detailsList)
        elif field == "userId":
            if spec == "all":
                occupiedSlots = OccupiedSlot.query.all()
            else:
                occupiedSlots = OccupiedSlot.query.filter_by(userId=spec).all()
            if not occupiedSlots:
                return {'message': 'No occupied slots found for this user'}, 202
            for occupied in occupiedSlots:
                name = User.query.filter_by(userId=occupied.userId).first()
                detailsList.append({
                    "userId": occupied.userId,
                    "userName": name.name,
                    "email": name.email,
                    "lotId": occupied.lotId,
                    "slotId": occupied.slotId,
                    "vehicleNo": occupied.vehicleNo,
                    "startTime": occupied.startTime.strftime('%Y-%m-%d %H:%M:%S'),
                    "endTime": occupied.endTime.strftime('%Y-%m-%d %H:%M:%S'),
                    "price": occupied.price
                })
            print(detailsList)
            return jsonify(detailsList)
        
class ApiBookSlot(Resource):
    @jwt_required()
    def get(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        userId=user.userId if user else None
        if not user:
            return {'message': 'Unauthorized'}, 401
        print(userId)
        occupied_slots = OccupiedSlot.query.filter_by(userId=userId).all()
        bookedDetails=[]
        for occupied_slot in occupied_slots:
            location=Lots.query.filter_by(lotId=occupied_slot.lotId).first()
            bookedDetails.append({
                "location": location.location if location else "Unknown",
                "lotId": occupied_slot.lotId,
                "slotId": occupied_slot.slotId, 
                "vehicleNo": occupied_slot.vehicleNo,
                "startTime": occupied_slot.startTime.strftime('%Y-%m-%d %H:%M:%S'),
                "endTime": occupied_slot.endTime.strftime('%Y-%m-%d %H:%M:%S'),
                "price": occupied_slot.price
            })
        print(bookedDetails)
        return jsonify({"bookedDetails":bookedDetails})
    @jwt_required()
    def post(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user:
            return {'message': 'Unauthorized'}, 401

        data = request.get_json()
        lotId = data.get('lotId')
        vehicleNo = data.get('vehicleNo')
        startTime = data.get('startTime')
        endTime = data.get('endTime')
        startDate = data.get('startDate')
        endDate = data.get('endDate')
        price = data.get('price')

        if not all([lotId, vehicleNo, startTime, endTime, startDate, endDate, price]):
            return {'message': 'Missing fields'}, 400

        try:
            dt_fmt = "%Y-%m-%d %H:%M"
            start_dt = datetime.strptime(f"{startDate} {startTime}", dt_fmt)
            end_dt = datetime.strptime(f"{endDate} {endTime}", dt_fmt)
            if start_dt >= end_dt:
                print("hi")
                return {'message': 'Invalid timestamp: Start time must be before End time'}, 200
        except Exception as e:
            print("hello")
            return {'message': f'Time parsing error: {str(e)}'}, 404

        slots = Slots.query.filter_by(lotId=lotId).order_by(Slots.slotId).all()
        for slot in slots:
            if not slot.isOccupied:
                slot.isOccupied = True
                db.session.add(slot)
                occupied_slot = OccupiedSlot(userId=user.userId,lotId=lotId,slotId=slot.slotId,vehicleNo=vehicleNo,price=price,startTime=start_dt,endTime=end_dt)
                db.session.add(occupied_slot)
                db.session.commit()
                return {"message": f'Slot {slot.slotId} booked insuccessfully', 'success': True}, 200

        return {"message": 'No available slots'}, 200
    def delete(self):
        data = request.get_json()
        lotId = data.get('lotId')
        slotId = data.get('slotId')
        occupied_slot = OccupiedSlot.query.filter_by(lotId=lotId, slotId=slotId).first()
        slots= Slots.query.filter_by(lotId=lotId, slotId=slotId).first()
        slots.isOccupied = False
        db.session.add(slots)
        db.session.delete(occupied_slot)
        db.session.commit()
        return {"message": f'Slot {slotId} in lot {lotId} deleted successfully'}, 200
    
class ApiSendMail(Resource):
    @jwt_required()
    def post(self):
        data=request.get_json()
        choice=data.get("choice")
        current_user_email=get_jwt_identity()
        user=User.query.filter_by(email=current_user_email).first()
        if choice=="bookLot":
            #--details--
            lotId=data.get("lotId")
            price=data.get("price")
            vehicleNo=data.get("vehicleNo")
            location=data.get("location")
            #----EMAIL----
            bodyMsg = f"Hi {user.name},\nYour slot has been successfully booked.\nLocation: {location}\nLot ID: {lotId}\nPrice: {price}\nVehicle No: {vehicleNo}\nThank you for using our service!"
            recipients=[f"{user.email}"]
            subject="Booking Of Lots"
            
        elif choice=="createLot":
            #-details---
            lotId=data.get("lotId")
            location=data.get("location")
            price=data.get("price")
            maxSlots=data.get("maxSlots")
            
            #---EMAIL---
            users=User.query.all()
            recipients=[]
            for user in users:
                if user.userId!=100000:
                    recipients.append(f"{user.email}")
            bodyMsg=f"A new parking lot has been created!\nLocation: {location}\nLot ID: {lotId}\nPrice:{price}\nMax Slots:{maxSlots}\nCheck it out in your app!"
            subject="Creation of New Lot !!"
        send_mail(subject,recipients,bodyMsg)
        return "mail sent succesfilly"
             
class ApiCharts(Resource):
    def get(self,choice):
        if choice=="user":
            locations = Locations.query.all()

            bar_data = []
            total_occupied = 0
            total_non_occupied = 0

            for loc in locations:
                lots = Lots.query.filter_by(location=loc.location).all()
                loc_total = 0
                loc_occupied = 0

                for lot in lots:
                    slots = Slots.query.filter_by(lotId=lot.lotId).all()
                    loc_total += len(slots)
                    loc_occupied += sum(1 for slot in slots if slot.isOccupied)

                loc_non_occupied = loc_total - loc_occupied

                bar_data.append({
                    'location': loc.location,
                    'occupied': loc_occupied,
                    'non_occupied': loc_non_occupied
                })

                total_occupied += loc_occupied
                total_non_occupied += loc_non_occupied

            response = {
                'bar_chart': bar_data,
                'pie_chart': {
                    'occupied': total_occupied,
                    'non_occupied': total_non_occupied
                }
            }

            return jsonify(response)
        if choice=="admin":
            locations = Locations.query.all()

            bar_data = []
            revenue_data = []
            total_occupied = 0
            total_non_occupied = 0

            for loc in locations:
                lots = Lots.query.filter_by(location=loc.location).all()
                loc_total = 0
                loc_occupied = 0
                loc_revenue = 0

                for lot in lots:
                    slots = Slots.query.filter_by(lotId=lot.lotId).all()
                    loc_total += len(slots)
                    loc_occupied += sum(1 for slot in slots if slot.isOccupied)

                    # Calculate revenue from OccupiedSlot
                    occupied = OccupiedSlot.query.filter_by(lotId=lot.lotId).all()
                    loc_revenue += sum(item.price for item in occupied)

                bar_data.append({
                    'location': loc.location,
                    'occupied': loc_occupied,
                    'non_occupied': loc_total - loc_occupied
                })

                revenue_data.append({
                    'location': loc.location,
                    'revenue': round(loc_revenue, 2)
                })

                total_occupied += loc_occupied
                total_non_occupied += loc_total - loc_occupied

            return jsonify({
                'bar_chart': bar_data,
                'pie_chart': {
                    'occupied': total_occupied,
                    'non_occupied': total_non_occupied
                },
                'revenue_chart': revenue_data
            })



@app.route('/reports/<filename>')
def download_report(filename):
    return send_from_directory('reports', filename, as_attachment=True)
       
                    



            
