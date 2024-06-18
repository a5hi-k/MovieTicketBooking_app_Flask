from flask import Blueprint
from flask import Flask, render_template
from flask import Flask, render_template, request, redirect,url_for,flash
from .models import User
from .db import db
from flask_login import login_required,login_user,logout_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash






admin_auth_routes=Blueprint("admin_auth_routes",__name__)



@admin_auth_routes.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        admin_username = request.form.get("username")
        admin_password = request.form.get("password")

        user = User.query.filter_by(username=admin_username).first()
        
        if user:
            if user.role == 'admin':
                if check_password_hash(user.password, admin_password):
                    flash("Logged in!", category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('admin_controll_routes.admin_home'))
                else:
                    flash('Wrong password!', category='error')
            else:
                flash("Permission Denied!", category='error')        
        else:
            flash('Admin not found', category='error')

    return render_template("admin_login.html", user=current_user)



@admin_auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("user_auth_routes.user_login"))

