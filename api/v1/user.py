import config
from sqlite3 import *
import re
import os
import hashlib


class User:

    @staticmethod
    def create_table():
        connection = connect(config.db_file)
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (user_id integer PRIMARY KEY, name TEXT, email TEXT, password TEXT)""")
        connection.close()
        return True

    @staticmethod
    def exists(email, password, user_id=None):
        """ Retuns a boolean """
        connection = connect(config.db_file)
        if user_id is None:
            hashed_password = User.hashPassword(password)
            query = "SELECT COUNT(*) FROM users WHERE email=? AND password=?"
            count = connection.execute(
                query, (email, hashed_password)).fetchone()[0]
        else:
            query = "SELECT COUNT(*) FROM users WHERE user_id = ?"
            count = connection.execute(
                query, (user_id)).fetchone()[0]
        connection.close()
        return bool(count > 0)

    @staticmethod
    def get(user_id):
        """ 
            Get a single user based on passed user_id,
            We should check that it is not null and it's a positive number.
        """
        conn = connect(config.db_file)
        if User.exists(user_id) == True:
            query = f"SELECT * FROM users WHERE user_id={user_id}"
            user = conn.execute(query).fetchone()
            conn.close()
            return {'user_id': user[0], 'name': user[1],
                    'email': user[2], 'password': user[3]}
        else:
            return False

    @staticmethod
    def isAValidEmail(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    @staticmethod
    def hashPassword(password):
        # salt = os.urandom(16)
        password = password.encode('utf-8')
        salt = b"SelfEvaluator"
        return hashlib.pbkdf2_hmac(
            'sha256', password, salt, 100000)

    @staticmethod
    def add(name, email, password):
        """check if the passed data is correct and add the user if does not already exists. check id based on given email address"""
        if User.exists(email, password) is not True:
            if User.isAValidEmail(email):
                # Hash password
                hashed_password = User.hashPassword(password)
                connection = connect(config.db_file)
                cursor = connection.cursor()
                query = f"INSERT INTO users (name,email,password) VALUES (?, ?, ?)"
                cursor.execute(query, (name, email, hashed_password))
                connection.commit()
                connection.close()
                return True
        return False

    @staticmethod
    def update(user_id, name, email, password):
        # TODO: update Email needs to be confirmed by the Email owner, so this feature will stand by
        if User.exists(user_id) and len(name) > 3 and len(password) > 3:
            hashed_password = User.hashPassword(password)
            connection = connect(config.db_file)
            cursor = connection.cursor()
            query = f"UPDATE users SET name = '{name}', password = '{hashed_password}' WHERE user_id = {user_id} LIMIT 1"
            cursor.execute(query)
            connection.commit()
            connection.close()
            return True
        return False

    @staticmethod
    def remove(user_id):
        connection = connect(config.db_file)
        cursor = connection.cursor()
        query = f"DELETE FROM users WHERE user_id = {user_id} LIMIT 1"
        cursor.execute()
        connection.commit()
        connection.close()
        return True
