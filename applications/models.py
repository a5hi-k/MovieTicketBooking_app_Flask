from .db import db
from sqlalchemy.sql import func
from flask_login import UserMixin







class User(db.Model,UserMixin):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(25),unique=True)
    password=db.Column(db.String)
    email=db.Column(db.String,unique=True)
    role=db.Column(db.String,default="user")
    review=db.relationship('Review',backref='user',passive_deletes=True)
    bookings=db.relationship('Booking',backref='user',passive_deletes=True)




class Venue(db.Model):    
    __tablename__='venue'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    location=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    capacity=db.Column(db.String,nullable=False)
    image=db.Column(db.String,nullable=False)
    additional_price=db.Column(db.Integer,default=0)
    shows=db.relationship("Venue_show",backref='venue',passive_deletes=True)
    bookings=db.relationship('Booking',backref='venue',passive_deletes=True)
    seats=db.relationship('Capacity',backref='venue',passive_deletes=True)





class Show(db.Model):
    __tablename__='show'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    poster=db.Column(db.String,nullable=False)
    trailer=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    rating=db.Column(db.Integer,default=0)
    ratecount=db.Column(db.Integer,default=0)
    tags=db.Column(db.String)
    date=db.Column(db.String,nullable=False)
    price=db.Column(db.Integer,nullable=False)
    reviews=db.relationship('Review',backref='show',passive_deletes=True)
    allocations=db.relationship("Venue_show",backref='show',passive_deletes=True)
    bookings=db.relationship('Booking',backref='show',passive_deletes=True)
    seats=db.relationship('Capacity',backref='show',passive_deletes=True)


class Venue_show(db.Model):
    __tablename__='venue_show'
    id=db.Column(db.Integer,primary_key=True)
    venue_id=db.Column(db.Integer,db.ForeignKey('venue.id',ondelete="CASCADE"))
    show_id=db.Column(db.Integer,db.ForeignKey('show.id',ondelete="CASCADE"))




class Review(db.Model):
    __tablename__='review'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(40), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id', ondelete="CASCADE"), nullable=False)







class Booking(db.Model):
    __tablename__='booking'
    id=db.Column(db.Integer,primary_key=True)
    person=db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"))
    place=db.Column(db.Integer,db.ForeignKey('venue.id',ondelete="CASCADE"))
    movie=db.Column(db.Integer,db.ForeignKey('show.id',ondelete="CASCADE"))
    seats=db.Column(db.Integer)
    price=db.Column(db.Integer)
    date=db.Column(db.String)
    capacity=db.Column(db.Integer)



class Capacity(db.Model):
    __tablename__='capacity'
    id=db.Column(db.Integer,primary_key=True)
    place=db.Column(db.Integer,db.ForeignKey('venue.id',ondelete="CASCADE"))
    movie=db.Column(db.Integer,db.ForeignKey('show.id',ondelete="CASCADE"))
    date=db.Column(db.String)
    current_capacity=db.Column(db.Integer)


    
