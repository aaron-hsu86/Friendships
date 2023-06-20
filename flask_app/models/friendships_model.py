from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import friendships_model
from flask import flash

class Friendships:

    DB = 'friendships_schema'
    tables = 'friendships'

    def __init__(self, data) -> None:
        self.id = data['id']
        self.user_id = data['user_id']
        self.friend_id = data['friend_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = f'SELECT * FROM {cls.tables};'
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        if results:
            for user in results:
                users.append( cls(user) )
        return users
    
    @classmethod
    def get_one(cls, id):
        query = f'SELECT * FROM {cls.tables} WHERE id = %(id)s;'
        data={'id':id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results)< 1:
            return False
        return cls(results[0])
    
    @classmethod
    def save(cls, data):
        query = f'''INSERT INTO {cls.tables} 
                (user_id, friend_id) 
                VALUES (  %(user_id)s, %(friend_id)s  );'''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = f'''UPDATE {cls.tables} SET
                user_id = %(user_id)s, 
                friend_id = %(friend_id)s
                WHERE id = %(id)s;'''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete(cls, id):
        query = f'DELETE FROM {cls.tables} WHERE id = %(id)s;'
        data = {'id' : id}
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_friendships(cls):
        query = '''SELECT * FROM friendships
                LEFT JOIN users ON users.id = user_id
                LEFT JOIN users AS friends ON friends.id = friend_id;'''
        results = connectToMySQL(cls.DB).query_db(query)
        friendships = []
        if results:
            for friends in results:
                # print(friends)
                data = {
                    'id': friends['id'],
                    'user_first_name': friends['first_name'],
                    'user_last_name': friends['last_name'],
                    'friend_first_name': friends['friends.first_name'],
                    'friend_last_name': friends['friends.last_name']
                }
                friendships.append( data )
        return friendships
        
    @classmethod
    def check_relationships(cls, form):
        query = 'SELECT friend_id FROM friendships WHERE user_id = %(id)s;'
        user_id = form['user_id']
        friend_id = int(form['friend_id'])
        data = {'id' : user_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        friends = []
        if results:
            for friend in results:
                friends.append(friend['friend_id'])
        not_friends = True
        for friend in friends:
            if friend_id == friend:
                not_friends = False
        return not_friends

    @staticmethod
    def relationship_form_check(form):
        is_valid = True
        if "user_id" not in form:
            flash('Please select a user')
            is_valid = False
        if 'friend_id' not in form:
            flash('Please select a friend')
            is_valid = False
        return is_valid