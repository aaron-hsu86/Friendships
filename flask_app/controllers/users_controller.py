from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import users_model, friendships_model

@app.route('/')
@app.route('/friendships')
def main_page():
    users = users_model.Users.get_all()
    friends = users
    friendships = friendships_model.Friendships.get_friendships()
    return render_template('index.html', users=users, friends=friends, friendships = friendships)

@app.route('/add_user', methods=['post'])
def add_user():
    print(request.form)
    if not users_model.Users.va:
        return redirect('/friendships')
    users_model.Users.save(request.form)
    return redirect('/friendships')

@app.route('/create_friendship', methods=['post'])
def create_friendship():
    if not friendships_model.Friendships.relationship_form_check(request.form):
        return redirect('/friendships')

    if not friendships_model.Friendships.check_relationships(request.form):
        flash('They are already friends!')
        return redirect('/friendships')
    friendships_model.Friendships.save(request.form)

    return redirect('/friendships')

@app.route('/delete_friendship/<int:friends_id>')
def delete_friendship(friends_id):
    friendships_model.Friendships.delete(friends_id)
    return redirect('/friendships')