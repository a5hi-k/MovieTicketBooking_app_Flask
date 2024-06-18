from flask import Blueprint
from flask import Flask, render_template, request, redirect,url_for,flash
from flask_login import login_required,current_user
import os,secrets
from .models import Venue,Show,Venue_show,Booking
from flask import current_app as app
from .db import db
from sqlalchemy import or_
import matplotlib.pyplot as plt







admin_controll_routes=Blueprint("admin_controll_routes",__name__)





image_files = set(['png','jpg','jpeg'])
video_files = set(['mp4'])
def supporting_image_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in image_files

def supporting_video_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in video_files


def file_processing(file):
    hashed_name = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(file.filename)
    new_name = hashed_name + f_ext

    return new_name ,f_ext   






@admin_controll_routes.route('/admin_home',methods=['GET','POST'])
@login_required
def admin_home():
    if current_user.role == 'admin':

        venues=Venue.query.order_by(Venue.id.desc())

        return render_template('admin_home.html',user=current_user,venues=venues)
    else:
        flash("You don't have permission to view this page",category='error')
        return redirect(url_for('user_controll_routes.user_home'))






@admin_controll_routes.route('/add_venue',methods=['GET','POST'])
@login_required
def add_venue():
    if current_user.role == 'admin':

        if request.method=="POST":
            name=request.form.get('name')
            location=request.form.get('location')
            capacity=request.form.get('capacity')
            description=request.form.get('description')
            additional_price=request.form.get('additional_price')
            file=request.files['file']

            if not name or not location or  not capacity or not description:
                flash('Some details are missing', category='error')
            elif not capacity.isnumeric():
                flash('capacity should be numeric',category='error')
            elif file.filename=='':
                flash('no image is selected for uploading',category='error')
            elif supporting_image_file(file.filename):
                image,type=file_processing(file) 
                picture_path=os.path.join(app.root_path,'static/venue_images',image)
            
                file.save(picture_path)
            
                new_venue = Venue(name=name,location=location,description=description,capacity=capacity,additional_price=additional_price,image=image)
                db.session.add(new_venue)
                db.session.commit()
                flash('New venue added sucessfully!', category='success')
                return redirect(url_for('admin_controll_routes.admin_home'))
            else:
                flash('only jpg,jpeg and png files are allowed',category='error')    
        

        return render_template('add_venue.html',user=current_user)
    else:
        flash("Permission Denied",category='error')
        return redirect(url_for('user_controll_routes.user_home'))






@admin_controll_routes.route('/avenue_shows/<venue_id>',methods=['GET','POST'])
@login_required
def avenue_shows(venue_id):
    if current_user.role == 'admin':

        venue=Venue.query.filter_by(id=venue_id).first()

        if not venue:
            flash("venue does not exist",category='error')
            return redirect(url_for('admin_controll_routes.admin_home'))

           
        shows=Venue_show.query.filter_by(venue_id=venue.id).order_by(Venue_show.id.desc())

        return render_template('avenue_shows.html',user=current_user,venue=venue,shows=shows)
    else:
        flash("You don't have permission to view this page",category='error')
        return redirect(url_for('user_controll_routes.user_home'))







@admin_controll_routes.route('/aview_show/<show_id>',methods=['GET','POST'])
@login_required
def aview_show(show_id):
    if current_user.role == 'admin':

        show=Show.query.filter_by(id=show_id).first()

        if not show:
            flash("show does not exist",category='error')
            return redirect(url_for('admin_controll_routes.admin_home'))

           

        return render_template('aview_show.html',user=current_user,show=show)
    else:
        flash("You don't have permission to view this page",category='error')
        return redirect(url_for('user_controll_routes.user_home'))








@admin_controll_routes.route('/add_show',methods=['GET','POST'])
@login_required
def add_show():
    if current_user.role == 'admin':

        venues=Venue.query.all()

        if request.method=="POST":
            name=request.form.get('name')
            date=request.form.get('date')
            price=request.form.get('price')
            tags=request.form.get('tags')
            description=request.form.get('description')
            poster=request.files['poster']
            trailer=request.files['trailer']
            venue_list=request.form.getlist('items')


            if not name or not date or  not price or not tags or not description:
                flash('Some details are missing', category='error')
            elif not price.isnumeric():
                flash('price should be numeric',category='error')
            elif poster.filename=='' or trailer.filename=='':
                flash('no image or trailer is selected for uploading',category='error')
            elif supporting_image_file(poster.filename) and supporting_video_file(trailer.filename):
                image,type=file_processing(poster)
                video,type=file_processing(trailer) 
                picture_path=os.path.join(app.root_path,'static/show_images',image)
                trailer_path=os.path.join(app.root_path,'static/show_trailers',video)
            
                poster.save(picture_path)
                trailer.save(trailer_path)

            
                new_show = Show(name=name,date=date,price=price,tags=tags,description=description,poster=image,trailer=video)
                db.session.add(new_show)
                db.session.commit()

                show_id=new_show.id
                if venue_list != []:
                    for id in venue_list:
                        venue=Venue.query.filter_by(id=int(id)).first()
                        newentry=Venue_show(venue_id=int(id),show_id=show_id)
                        db.session.add(newentry)
                    db.session.commit()
                flash('New show added sucessfully!', category='success')
                return redirect(url_for('admin_controll_routes.admin_home'))
            else:
                flash('file upload error,make sure poster is a jpg,jepg or png file and trailer is a mp4 file',category='error')    
        


        return render_template('add_show.html',user=current_user,venues=venues)
    else:
        flash("Permission Denied",category='error')
        return redirect(url_for('user_controll_routes.user_home'))




@admin_controll_routes.route('/update_show/<show_id>',methods=['GET','POST'])
@login_required
def update_show(show_id):
    if current_user.role == 'admin':

        show=Show.query.filter_by(id=show_id).first()

        if not show:
            flash("show does not exist",category='error')
            return redirect(url_for('admin_controll_routes.admin_home'))

        allocations=Venue_show.query.filter_by(show_id=show.id).all()
        venues=Venue.query.all()
        list=[]
        for i in allocations:
            list.append(i.venue_id)

        if request.method=="POST":
            name=request.form.get('name')
            date=request.form.get('date')
            price=request.form.get('price')
            tags=request.form.get('tags')
            description=request.form.get('description')
            poster=request.files['poster']
            trailer=request.files['trailer']
            venue_list=request.form.getlist('items')


            if poster:
                old_poster=show.poster
                if poster.filename=='':
                    flash('no image is selected for uploading',category='error')
                    return redirect(url_for('admin_controll_routes.update_show',show_id=show.id))
                elif supporting_image_file(poster.filename):
                            image,type=file_processing(poster) 
                            picture_path=os.path.join(app.root_path,'static/show_images',image)
                            os.remove(os.path.join(app.root_path,'static/show_images',old_poster))

                            poster.save(picture_path)

                            show.poster=image
                            db.session.commit()



                else:
                    flash('only jpg,jpeg and png files are allowed',category='error')    
                    return redirect(url_for('admin_controll_routes.update_show',show_id=show.id))



            if trailer:
                old_trailer=show.trailer
                if trailer.filename=='':
                    flash('no video is selected for uploading',category='error')
                    return redirect(url_for('admin_controll_routes.update_show',show_id=show.id))
                elif supporting_video_file(trailer.filename):
                            video,type=file_processing(trailer) 
                            video_path=os.path.join(app.root_path,'static/show_trailers',video)
                            os.remove(os.path.join(app.root_path,'static/show_trailers',old_trailer))

                            trailer.save(video_path)

                            show.trailer=video
                            db.session.commit()



                else:
                    flash('only mp4 files are allowed',category='error')    
                    return redirect(url_for('admin_controll_routes.update_show',show_id=show.id))


            for i in allocations:
                db.session.delete(i)
            db.session.commit()


            show.name=name
            show.date=date
            show.price=price
            show.tags=tags
            show.description=description

            db.session.commit()

            if venue_list != []:
                for id in venue_list:
                    # venue=Venue.query.filter_by(id=int(id)).first()
                    newentry=Venue_show(venue_id=int(id),show_id=show.id)
                    db.session.add(newentry)
                db.session.commit()





            flash('Updated sucessfully!', category='success')
            return redirect(url_for('admin_controll_routes.update_show',show_id=show.id))
        

        return render_template('update_show.html',user=current_user,show=show,allocations=allocations,venues=venues,list=list)
    else:
        flash("Permission Denied!",category='error')
        return redirect(url_for('user_controll_routes.user_home'))






@admin_controll_routes.route('/update_venue/<venue_id>',methods=['GET','POST'])
@login_required
def update_venue(venue_id):
    if current_user.role == 'admin':

        venue=Venue.query.filter_by(id=venue_id).first()

        if not venue:
            flash("venue does not exist",category='error')
            return redirect(url_for('admin_controll_routes.admin_home'))

        allocations=Venue_show.query.filter_by(venue_id=venue.id).all()
        shows=Show.query.all()
        list=[]
        for i in allocations:
            list.append(i.show_id)

        if request.method=="POST":
            name=request.form.get('name')
            location=request.form.get('location')
            capacity=request.form.get('capacity')
            description=request.form.get('description')
            additional_price=request.form.get('additional_price')
            image=request.files['file']
            show_list=request.form.getlist('items')


            if image:
                old_image=venue.image
                if image.filename=='':
                    flash('no image is selected for uploading',category='error')
                    return redirect(url_for('admin_controll_routes.update_venue',venue_id=venue.id))
                elif supporting_image_file(image.filename):
                            Image,type=file_processing(image) 
                            picture_path=os.path.join(app.root_path,'static/venue_images',Image)
                            os.remove(os.path.join(app.root_path,'static/venue_images',old_image))

                            image.save(picture_path)

                            venue.image=Image
                            db.session.commit()



                else:
                    flash('only jpg,jpeg and png files are allowed',category='error')    
                    return redirect(url_for('admin_controll_routes.update_show',venue_id=venue.id))



            for i in allocations:
                db.session.delete(i)
            db.session.commit()


            venue.name=name
            venue.location=location
            venue.capacity=capacity
            venue.description=description
            venue.additional_price=additional_price

            db.session.commit()

            if show_list != []:
                for id in show_list:
                    newentry=Venue_show(venue_id=venue.id,show_id=int(id))
                    db.session.add(newentry)
                db.session.commit()





            flash('Updated sucessfully!', category='success')
            return redirect(url_for('admin_controll_routes.update_venue',venue_id=venue.id))
        

        return render_template('update_venue.html',user=current_user,venue=venue,allocations=allocations,shows=shows,list=list)
    else:
        flash("Permission Denied!",category='error')
        return redirect(url_for('user_controll_routes.user_home'))







@admin_controll_routes.route('/delete_venue/<venue_id>',methods=['GET','POST'])
@login_required
def delete_venue(venue_id):
    if current_user.role == 'admin':

        venue=Venue.query.filter_by(id=venue_id).first()
        if not venue:
            flash("venue does not exist",category='error')
            return redirect(url_for('admin_controll_routes.admin_home'))



        db.session.delete(venue)
        db.session.commit()

        os.remove(os.path.join(app.root_path,'static/venue_images',venue.image))

        flash('Venue deleted',category='success')
        return redirect(url_for('admin_controll_routes.admin_home'))
    else:
        flash("Permission Denied!",category='error')
        return redirect(url_for('user_controll_routes.user_home'))






@admin_controll_routes.route('/delete_show/<show_id>',methods=['GET','POST'])
@login_required
def delete_show(show_id):
    if current_user.role == 'admin':

        show=Show.query.filter_by(id=show_id).first()
        if not show:
            flash("show does not exist",category='error')
            return redirect(url_for('admin_controll_routes.admin_home'))


        db.session.delete(show)
        db.session.commit()

        os.remove(os.path.join(app.root_path,'static/show_images',show.poster))
        os.remove(os.path.join(app.root_path,'static/show_trailers',show.trailer))

        flash('Show deleted',category='success')
        return redirect(url_for('admin_controll_routes.admin_home'))
    else:
        flash("Permission Denied!",category='error')
        return redirect(url_for('user_controll_routes.user_home'))




@admin_controll_routes.route("/usearch_shows", methods=['GET','POST'])
@login_required
def usearch_shows():

    text=request.form.get("text")

    query="%"+str(text)+"%"

    if text == 'all shows':
        shows=Show.query.order_by(Show.id.desc())
    else:    

        shows=Show.query.filter(or_(Show.name.like(query), Show.tags.like(query))).all()

    return render_template('ushows.html',user=current_user,shows=shows)







@admin_controll_routes.route("/global_booking_report", methods=['GET','POST'])
@login_required
def global_booking_report():
    if current_user.role == 'admin':


        bookings=Booking.query.all()
        venues=Venue.query.order_by(Venue.id.desc())

        dic={}
        for booking in bookings:
            if booking.show.name not in dic:
                dic[booking.show.name] = int(booking.seats)
            else:
                dic[booking.show.name] = dic[booking.show.name] + int(booking.seats)
      
        
        shows=list(dic.keys())
        books=list(dic.values())

        plt.bar(shows,books)

        plt.title('Global Show-Booking Status')
        plt.xlabel('Shows')
        plt.ylabel('Bookings')


        plt.savefig('global.png')

        flash('Report is successfully prepared',category='success')
        return render_template('admin_home.html',user=current_user,venues=venues)
    flash('Not available',category='error')    
    return redirect(url_for('user_controll_routes.user_home'))

