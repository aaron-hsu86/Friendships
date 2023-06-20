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
    is_valid = True
    if len(request.form['first_name']) < 3:
        flash('First Name must be at least 3 characters')
        is_valid = False
    if len(request.form['last_name']) < 3:
        flash('Last Name must be at least 3 characters')
        is_valid = False
    if not is_valid:
        return redirect('/friendships')
    users_model.Users.save(request.form)
    return redirect('/friendships')

@app.route('/create_friendship', methods=['post'])
def create_friendship():
    is_valid = True
    if "user_id" not in request.form:
        flash('Please select a user')
        is_valid = False
    if 'friend_id' not in request.form:
        flash('Please select a friend')
        is_valid = False
    if not is_valid:
        return redirect('/friendships')
    user_id = request.form['user_id']
    friend_id = int(request.form['friend_id'])
    friends_list = friendships_model.Friendships.check_relationships(user_id)
    already_friends = False
    for friend in friends_list:
        if friend_id == friend:
            already_friends = True
    if not already_friends:
        friendships_model.Friendships.save(request.form)
    else:
        flash('They are already friends!')
    return redirect('/friendships')

@app.route('/delete_friendship/<int:friends_id>')
def delete_friendship(friends_id):
    friendships_model.Friendships.delete(friends_id)
    return redirect('/friendships')