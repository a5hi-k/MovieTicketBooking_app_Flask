from flask import Blueprint
from flask import Flask, render_template, request, redirect,url_for,flash
from flask_login import login_required,current_user
from .models import User,Venue,Show,Review,Booking,Venue_show,Capacity
from .db import db
from sqlalchemy import or_
from flask_mail import *
from flask import current_app as app

mail=Mail(app)




user_controll_routes=Blueprint("user_controll_routes",__name__)


@user_controll_routes.route('/')
@user_controll_routes.route('/home',methods=['GET','POST'])
@login_required
def user_home():

    venues=Venue.query.all()
    shows=Show.query.order_by(Show.id.desc()).all()


    latest=Show.query.order_by(Show.id.desc()).limit(3).all()
    horror=Show.query.filter(Show.tags.like("%horror%")).all()
    romance=Show.query.filter(Show.tags.like("%romance%")).all()
    animae=Show.query.filter(Show.tags.like("%animae%")).all()



    return render_template('user_home.html',user=current_user,venues=venues,shows=shows,latest=latest,horror=horror,romance=romance,animae=animae)




@user_controll_routes.route('/venue_shows/<venue_id>',methods=['GET','POST'])
@login_required
def venue_shows(venue_id):
    venue=Venue.query.filter_by(id=venue_id).first()
    shows=Venue_show.query.filter_by(venue_id=venue_id).order_by(Venue_show.id.desc())

    
    if not venue:
        flash('Venue does not exist!.', category='error')
        return redirect(url_for('user_controll_routes.user_home'))

    return render_template('venue_shows.html',user=current_user,venue=venue,shows=shows)    




@user_controll_routes.route('/view_show/<show_id>',methods=['GET','POST'])
@login_required
def view_show(show_id):
    show=Show.query.filter_by(id=show_id).first()
    venues=Venue_show.query.filter_by(show_id=show_id)

    
    if not show:
        flash('Show does not exist!.', category='error')
        return redirect(url_for('user_controll_routes.user_home'))

    return render_template('view_show.html',user=current_user,show=show,venues=venues)    





@user_controll_routes.route("/review/<show_id>", methods=['POST'])
@login_required
def review(show_id):
    text = request.form.get('text')

    if not text:
        flash('Review cannot be empty.', category='error')
    else:
        show = Show.query.filter_by(id=show_id)
        if show:
            review = Review(text=text, author=current_user.id, show_id=show_id)
            db.session.add(review)
            db.session.commit()
        else:
            flash('Show does not exist.', category='error')

    return redirect(request.referrer)








@user_controll_routes.route("/review/delete/<review_id>")
@login_required
def delete_review(review_id):
    review = Review.query.filter_by(id=review_id).first()

    if not review:
        flash('Review does not exist.', category='error')
    elif current_user.id == review.author:
        db.session.delete(review)
        db.session.commit()
    else:
        flash('You do not have permission to delete this comment.', category='error')

    return redirect(request.referrer)





@user_controll_routes.route("/rate/<show_id>", methods=['POST'])
@login_required
def rate(show_id):
    num = request.form.get('rate')

    if not num:
        flash('Rating cannot be empty.', category='error')
    else:
        show = Show.query.filter_by(id=show_id).first()
        if show:

            show.rating += int(num)
            show.ratecount += 1


            db.session.commit()
        else:
            flash('Show does not exist.', category='error')

    return redirect(request.referrer)









def check(venue_id,show_id,date,seats):

    fvalue="none"
    try:
        availability=Capacity.query.filter_by(place=venue_id,movie=show_id,date=date).first()

        if availability:
            fvalue = availability.current_capacity - int(seats)


    except TypeError :
       fvalue = "none"


    return fvalue    








@user_controll_routes.route("/availability/<venue_id>/<show_id>", methods=['GET','POST'])
@login_required
def availability(venue_id,show_id):


    venue=Venue.query.filter_by(id=venue_id).first()
    show=Show.query.filter_by(id=show_id).first()
    venue_shows=Venue_show.query.filter_by(venue_id=venue_id).order_by(Venue_show.id.desc())

    if not venue or not show:
        flash('Not Found', category='error')
        return redirect(request.referrer)


    if request.method == 'POST':

        seats=request.form.get('seats')
        date=request.form.get('date')

        if not seats or not date:
            flash('Please enter seats and date for the show',category='error')
            return redirect(url_for('user_controll_routes.availability',venue_id=venue.id,show_id=show.id))

        Cap=Capacity.query.filter_by(place=venue_id,movie=show_id,date=date).first()

        value = check(venue_id,show_id,date,seats)

        if value != "none":
            if value < 0:
                flash('Not enough seats are available',category='error')
                return redirect(url_for('user_controll_routes.availability',venue_id=venue.id,show_id=show.id))

            if value == 0:
                flash('HouseFull!',category='error')
                return redirect(url_for('user_controll_routes.availability',venue_id=venue.id,show_id=show.id))

            cap=Cap.current_capacity
            return render_template('booking.html',user=current_user,venue=venue,show=show,date=date,seats=seats,cap=cap)
        else:
            cap = venue.capacity
            return render_template('booking.html',user=current_user,venue=venue,show=show,date=date,seats=seats,cap=cap)



    return render_template('availability.html',user=current_user,venue=venue,show=show,venue_shows=venue_shows)






@user_controll_routes.route("/booking/<user_id>/<venue_id>/<show_id>/<date>/<seats>", methods=['GET','POST'])
@login_required
def booking(user_id,venue_id,show_id,date,seats):

    venue=Venue.query.filter_by(id=venue_id).first()
    show=Show.query.filter_by(id=show_id).first()
    
    if not venue or not show:
        flash('Not Found', category='error')
        return redirect(request.referrer)

    if request.method == 'POST':    

        capacity=Capacity.query.filter_by(place=venue_id,movie=show_id,date=date).first()
            

        total_price=( (int(venue.additional_price) + int(show.price)) * int(seats) )


        if capacity:
            value = check(venue_id,show_id,date,seats)

            if value != "none":
                if value < 0:
                    flash('Not enough seats are available',category='error')
                    return redirect(url_for('user_controll_routes.availability',venue_id=venue.id,show_id=show.id))

                if value == 0:
                    flash('HouseFull!',category='error')
                    return redirect(url_for('user_controll_routes.availability',venue_id=venue.id,show_id=show.id))


            capacity.current_capacity -= int(seats)
            db.session.commit()
        else:
            new_entry=Capacity(place=venue_id,movie=show_id,date=date,current_capacity=(int(venue.capacity) - int(seats)))
            db.session.add(new_entry)
            db.session.commit()    

        existing_booking=Booking.query.filter_by(person=user_id,place=venue_id,movie=show_id,date=date).first()

        if existing_booking:
            existing_booking.seats += int(seats)
            existing_booking.price += int(total_price)
            db.session.commit()
        else:    

            new_booking=Booking(person=user_id,place=venue_id,movie=show_id,seats=seats,price=total_price,date=date)
            db.session.add(new_booking)
            db.session.commit()



        booking=Booking.query.filter_by(person=user_id,place=venue_id,movie=show_id,date=date).first()


        msg=Message('Successfull Booking!',sender='noreplay@gmail.com',recipients=[current_user.email])
        msg.body=f''' 
                    Your Booking for {booking.seats} seats for the movie "{booking.show.name}" on {booking.date} at {booking.venue.name} is successfull! 
                    Total price {booking.price} Thank you,{current_user.username} for booking at {booking.venue.name}'''

        try:                
            mail.send(msg)
        except:
            flash('Invalid email!',category='error')



        flash('Booking successfull',category='success')
        return render_template('ticket.html',user=current_user,booking=booking)





    return render_template('booking.html',user=current_user,venue=venue,show=show,date=date)








@user_controll_routes.route("/user_booking/<user_id>", methods=['GET'])
@login_required
def ticket(user_id):

    bookings=Booking.query.filter_by(person=user_id)

    return render_template('user_booking.html',user=current_user,bookings=bookings)




@user_controll_routes.route("/cancel_booking/<booking_id>", methods=['GET','POST'])
@login_required
def cancel_booking(booking_id):

    booking=Booking.query.filter_by(id=booking_id).first()
    bookings=Booking.query.filter_by(person=current_user.id)

    if not booking:
        flash('There is no such booking',category='error')
        return redirect(request.referrer)
    if booking.person != current_user.id:
        flash('Permission Denied!',category='error')
        return redirect(request.referrer)

    cap=Capacity.query.filter_by(place=booking.place,movie=booking.movie,date=booking.date).first()
    cap.current_capacity += int(booking.seats)

    db.session.delete(booking)
    db.session.commit()

    return render_template('user_booking.html',user=current_user,bookings=bookings)




@user_controll_routes.route("/search_shows", methods=['GET','POST'])
@login_required
def search_shows():

    text=request.form.get("text")

    query="%"+str(text)+"%"

    shows=Show.query.filter(or_(Show.name.like(query), Show.tags.like(query))).all()

    return render_template('shows.html',user=current_user,shows=shows)





@user_controll_routes.route("/search_venues", methods=['GET','POST'])
@login_required
def search_venues():

    text=request.form.get("text")

    query="%"+str(text)+"%"

    venues=Venue.query.filter(or_(Venue.name.like(query), Venue.location.like(query))).all()

    return render_template('venues.html',user=current_user,venues=venues)

