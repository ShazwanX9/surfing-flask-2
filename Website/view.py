from flask import Blueprint, render_template, url_for, redirect, flash, request, jsonify
from flask_login import login_required, current_user
from random import randrange
import json

from .dbmanip import User, Note, Feed
from .config import ConstData
from . import db

view = Blueprint("view", __name__)

@view.route("/",  methods=["GET", "POST"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for("view.user", name=current_user.username))
    else:
        return render_template( "index.html",
                                user=current_user )

@view.route("/<name>")
@login_required
def user(name):
    check_user = User.query.filter_by(username=name).first()
    if check_user:
        return render_template( "home.html", 
                        user=check_user, 
                        gender=("male", "female", None)[randrange(3)], 
                        randrange=randrange )

    flash("User Does Not Exist!", category='error')
    return redirect(url_for("view.user", name=current_user.username))

@view.route("/index")
@login_required
def index():
    return render_template("index.html", user=current_user)

@view.route("/contactUs")
@login_required
def chat():
    return render_template( "contactUs.html", 
                            user=current_user,
                            myName=ConstData.MY_NAME,
                            myEmail=ConstData.MY_EMAIL,
                            myPhone=ConstData.MY_PHONE,
                            randrange=randrange)

@view.route("/posting", methods=["GET", "POST"])
@login_required
def posting():
    if request.method == "POST":
        feed = request.form.get("text")
        new_feed = Feed(data=feed, user_id=current_user.id)
        db.session.add(new_feed)
        db.session.commit()
        flash('Feed added!', category='success')
    
    messages = []
    for item in sorted(Feed.query.all(), key=lambda x: x.date, reverse=True):
        messages.append({ "name": User.query.get(item.user_id).username, 
                          "data": item.data, 
                          "id": item.id,
                          "user_id": item.user_id })

    return render_template( "posting.html",
                             user=current_user,
                             messages=list(reversed(messages)),
                             enumerate=enumerate,
                             onFocusText="")

@view.route("/todolist", methods = ["GET", "POST"])
@login_required
def todolist():
    if request.method == "POST":
        note = request.form.get("text")
        new_note = Note(data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note added!', category='success')

    return render_template( "todolist.html",
                             user=current_user,
                             enumerate=enumerate)

################################################################################################

@view.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@view.route('/delete-feed', methods=['POST'])
def delete_feed():
    feed = json.loads(request.data)
    feedId = feed['feedId']
    feed = Feed.query.get(feedId)
    if feed:
        if feed.user_id == current_user.id:
            db.session.delete(feed)
            db.session.commit()

    return jsonify({})

################################################################################################