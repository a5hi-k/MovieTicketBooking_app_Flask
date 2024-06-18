from flask import Blueprint
from flask import Flask, render_template, request, redirect,url_for,flash
from flask_login import login_required,login_user,logout_user,current_user
from .models import User
from .db import db
from werkzeug.security import generate_password_hash,check_password_hash








user_auth_routes=Blueprint("user_auth_routes",__name__)





@user_auth_routes.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user_email=request.form.get("email")
        user_username=request.form.get("username")
        user_password1=request.form.get("password1")
        user_password2=request.form.get("password2")

        existing_email = User.query.filter_by(email=user_email).first()
        existing_username = User.query.filter_by(username=user_username).first()

        if existing_email:
            flash('This email already exist,Try another one!', category='error')
        elif existing_username:
            flash('This username already exist,try another one!', category='error')
        elif user_password1 != user_password2:
            flash('Please retype the password correctly', category='error')
        elif '@' not in user_email:
            flash("Email is invalid.", category='error')
        else:
            users=User.query.all()
            if users:
                new_user = User(email=user_email, username=user_username, password=generate_password_hash(user_password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
            else:
                new_user = User(email=user_email, username=user_username, password=generate_password_hash(user_password1, method='sha256'),role="admin")    
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)

            flash('User created sucessfully!',category='success')
            return redirect(url_for('user_controll_routes.user_home'))


    return render_template('register.html',user=current_user)





@user_auth_routes.route('/user_login',methods=['GET','POST'])
def user_login():
    if request.method == 'POST':
        user_username = request.form.get("username")
        user_password = request.form.get("password")

        user = User.query.filter_by(username=user_username).first()
        if user:
            if check_password_hash(user.password, user_password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('user_controll_routes.user_home'))
            else:
                flash('Wrong password!', category='error')
        else:
            flash('There is no such User!', category='error')

    return render_template("user_login.html", user=current_user)









@user_auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("user_auth_routes.user_login"))

