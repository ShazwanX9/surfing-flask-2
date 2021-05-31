from flask import Blueprint, render_template, url_for, redirect, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .dbmanip import User
from .view import view
from . import db

###########################################################################################

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login_phase():
    if request.method == "POST":
            text = request.form.get("text")
            pswd = request.form.get("password")
            remb = request.form.get("remember")
            # print(text, pswd, remb)

            # check text phone num / username / email
            checkUser = None
            if not checkUser:
                checkUser = User.query.filter_by(email=text).first()
            if not checkUser:
                checkUser = User.query.filter_by(username=text).first()
            if not checkUser:
                checkUser = User.query.filter_by(phoneNum=text).first()

            # check password
            if checkUser:
                if check_password_hash(checkUser.password, pswd):
                    flash('Logged in successfully!', category='success')
                    print('Logged in successfully!')
                    login_user(checkUser, remember=remb=="on")
                    return redirect(url_for("view.home"))
                else:
                    flash('Incorrect password, try again.', category='error')
                    print('Incorrect password, try again.')
            else:
                flash('Username does not exist.', category='error')
                print('Username does not exist.')

    if current_user.is_authenticated:
        return redirect(url_for("view.home"))
    return render_template ( "login.html", user=current_user )

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login_phase"))

@auth.route("/signUp", methods=["GET", "POST"])
def signUp():
    if request.method == "POST":
        email     = request.form.get("email")
        username  = request.form.get("username")
        phoneNum  = request.form.get("phoneNum")
        password1 = request.form.get("psw")
        password2 = request.form.get("psw-repeat")
        remember  = request.form.get("remember")

        # check text phone num / username / pass
        checkEmail  = User.query.filter_by(email=email).first()
        checkUser   = User.query.filter_by(username=username).first()
        checkPhone  = User.query.filter_by(phoneNum=phoneNum).first()

        # print(email, username, phoneNum, password1, password2)

        if checkEmail:
            flash("Email Alredy EXIST!", category="error")
        # elif '@' not in email:
        #     flash("Email is NOT Valid!", category="error")
        elif checkUser:
            flash("User Alredy EXIST!", category="error")
        elif checkPhone:
            flash("Phone Number Alredy REGISTERED!", category="error")
        elif password1 != password2:
            flash("Password didn't Match", category="error")
        else:
            # flash("Account Created!", category="success")
            print("Account Created!", password1)
            new_user = User(
                email=email, 
                username=username, 
                phoneNum=phoneNum, 
                password=generate_password_hash(password1, method="sha256")
                )
            # update database
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=remember=="on")
            return redirect(url_for("auth.login_phase"))

    if current_user.is_authenticated:
        return redirect(url_for("view.home"))


    return render_template ("signUp.html", user=current_user)


