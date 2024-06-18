from flask_restful import Resource,reqparse,fields,marshal_with,HTTPException
from flask import make_response
import json
from .db import db
from .models import Venue,Show



venue_fields={
    "id":fields.Integer,
    "name":fields.String,
    "location":fields.String,
    "description":fields.String,
    "capacity":fields.Integer,
    "image":fields.String,
    "additional_price":fields.Integer,
}
show_fields={
    "id":fields.Integer,
    "name":fields.String,
    "poster":fields.String,
    "trailer":fields.String,
    "description":fields.String,
    "rating":fields.Integer,
    "ratecount":fields.Integer,
    "tags":fields.String,
    "date":fields.String,
    "price":fields.Integer
}


create_venue_parser=reqparse.RequestParser()
create_venue_parser.add_argument('name')     
create_venue_parser.add_argument('location')
create_venue_parser.add_argument('description')
create_venue_parser.add_argument('capacity')
create_venue_parser.add_argument('image')
create_venue_parser.add_argument('additional_price')



update_venue_parser=reqparse.RequestParser()
update_venue_parser.add_argument('name')     
update_venue_parser.add_argument('location')
update_venue_parser.add_argument('description')
update_venue_parser.add_argument('capacity')
update_venue_parser.add_argument('image')
update_venue_parser.add_argument('additional_price')






create_show_parser=reqparse.RequestParser()
create_show_parser.add_argument('name')
create_show_parser.add_argument('poster')
create_show_parser.add_argument('trailer')
create_show_parser.add_argument('description')
create_show_parser.add_argument('rating')
create_show_parser.add_argument('ratecount')
create_show_parser.add_argument('tags')
create_show_parser.add_argument('date')
create_show_parser.add_argument('price')




update_show_parser=reqparse.RequestParser()
update_show_parser.add_argument('name')
update_show_parser.add_argument('poster')
update_show_parser.add_argument('trailer')
update_show_parser.add_argument('description')
update_show_parser.add_argument('tags')
update_show_parser.add_argument('date')
update_show_parser.add_argument('price')




class VenueAPI(Resource):    
# adding a new venue to venue table
    @marshal_with(venue_fields)
    def post(self):
        args=create_venue_parser.parse_args()
        name=args.get("name",None) 
        location=args.get("location",None)
        description=args.get("description",None)
        capacity=args.get('capacity',None)
        image=args.get("image",None)
        additional_price=args.get('additional_price',None)


        if name is None:
            raise BusinessValidationError(status_code=400,error_message="name is required")
        if location is None:
            raise BusinessValidationError(status_code=400,error_message="location is required")
        if description is None:
            raise BusinessValidationError(status_code=400,error_message="description is required")
        if capacity is None:
            raise BusinessValidationError(status_code=400,error_message="capacity is required")
        if image is None:
            raise BusinessValidationError(status_code=400,error_message="image is required")
        if not isinstance(capacity,(int)):
            raise BusinessValidationError(status_code=400,error_message="capacity should be numeric")
        if not isinstance(additional_price,(int)):
            raise BusinessValidationError(status_code=400,error_message="additional price should be numeric")


        new_venue=Venue(name=name,location=location,description=description,capacity=capacity,image=image,additional_price=additional_price)
        db.session.add(new_venue)
        db.session.commit()
        
        return new_venue,201
    
    # getting the details of the user
    @marshal_with(venue_fields)
    def get(self,venue_id):
        venue=db.session.query(Venue).filter(Venue.id==venue_id).first()
        if venue:
            return venue,200
        else:
            raise NotFoundError(status_code=404)



    # updating a venue
    @marshal_with(venue_fields)
    def put(self,venue_id):
        args=update_venue_parser.parse_args()
        name=args.get("name",None)
        location=args.get("location",None)
        description=args.get("description",None)
        capacity=args.get("capacity",None)
        image=args.get("image",None)
        additional_price=args.get("additional_price",None)


        venue=db.session.query(Venue).filter(Venue.id==venue_id).first()
        if not venue:
            raise NotFoundError(status_code=404)        

        if image:
            venue.image=image    

        
        venue.name=name
        venue.location=location
        venue.description=description
        venue.capacity=capacity
        venue.additional_price=additional_price

        db.session.commit()

        return venue,200

            
    # deleting a venue
    def delete(self,venue_id):
        venue=db.session.query(Venue).filter(Venue.id==venue_id).first()


        if venue is None:
            raise NotFoundError(status_code=404)

        db.session.delete(venue) 
        db.session.commit()
        
        return  200





class ShowAPI(Resource):    
# adding a new show to show table
    @marshal_with(show_fields)
    def post(self):
        args=create_show_parser.parse_args()
        name=args.get("name",None)
        poster=args.get("poster",None)
        trailer=args.get("trailer",None)
        description=args.get("description",None)
        tags=args.get("tags",None)
        date=args.get("date",None)
        price=args.get("price",None)

        if name is None:
            raise BusinessValidationError(status_code=400,error_message="name is required")
        if poster is None:
            raise BusinessValidationError(status_code=400,error_message="poster is required")
        if trailer is None:
            raise BusinessValidationError(status_code=400,error_message="trailer is required")
        if description is None:
            raise BusinessValidationError(status_code=400,error_message="description is required")
        if date is None:
            raise BusinessValidationError(status_code=400,error_message="date is required")
        if price is None:
            raise BusinessValidationError(status_code=400,error_message="price is required")
            
        new_show=Show(name=name,poster=poster,trailer=trailer,description=description,tags=tags,date=date,price=price)
        db.session.add(new_show)
        db.session.commit()
        
        return new_show,201
    

    # getting a show
    @marshal_with(show_fields)
    def get(self,show_id):
        show=db.session.query(Show).filter(Show.id==show_id).first()
        if not show:
            raise NotFoundError(status_code=404)
        return show, 200 


    # updating a show
    @marshal_with(show_fields)
    def put(self,show_id):
        args=update_show_parser.parse_args()
        name=args.get("name",None)
        poster=args.get("poster",None)
        trailer=args.get("trailer",None)
        description=args.get("description",None)
        tags=args.get("tags",None)
        date=args.get("date",None)
        price=args.get("price",None)

        show=db.session.query(Show).filter(Show.id==show_id).first()
        if not show:
            raise NotFoundError(status_code=404)

        if poster:
            show.poster=poster
        if trailer:
            show.trailer=trailer

        show.name=name
        show.description=description
        show.tags=tags
        show.date=date
        show.price=price

        db.session.commit()

        return show, 200

            
    # deleting a show
    def delete(self,show_id):


        show=db.session.query(Show).filter(Show.id==show_id).first()
        if show is None:
            raise NotFoundError(status_code=404)


        db.session.delete(show) 
        db.session.commit()
        
        return  200









class NotFoundError(HTTPException):
    def __init__(self, status_code):
        self.response=make_response('',status_code)




class BusinessValidationError(HTTPException):
    def __init__(self, status_code,error_message):
        message={"error_message":error_message}
        self.response=make_response(json.dumps(message),status_code)



