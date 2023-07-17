from sqlite3 import *

import config


class Result:

    @staticmethod
    def create_table():
        connection = connect(config.db_file)
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS results (id integer PRIMARY KEY, result TEXT, date DATE, user_id integer, FOREIGN KEY(user_id) REFERENCES user(user_id))""")
        connection.close()
        return True

    @staticmethod
    def get_all(user_id, limit=None):
        connection = connect(config.db_file)
        if limit is not None:
            query = "SELECT * FROM results WHERE user_id = ? LIMIT ?"
            results = connection.execute(query, (user_id, limit)).fetchall()
        else:
            query = "SELECT * FROM results WHERE user_id = ?"
            results = connection.execute(query, (user_id, )).fetchall()
        connection.close()
        the_results = []
        for result in results:
            result_dict = {'id': result[0],
                           'result': result[1], 'date': result[2]}
            the_results.append(result_dict)
        return the_results

    @staticmethod
    def get_count(user_id):
        conn = connect(config.db_file)
        query = "SELECT count(*) FROM results WHERE user_id = ?"
        count = conn.execute(query, (user_id,)).fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def exist(result_id):
        connection = connect(config.db_file)
        query = "SELECT COUNT (*) FROM results WHERE id= ?"
        count = connection.execute(query, (result_id,)).fetchone()[0]
        connection.close()
        if count > 0:
            return True
        else:
            return False

    @staticmethod
    def add(result, date, user_id):
        connection = connect(config.db_file)
        cursor = connection.cursor()
        query = 'INSERT INTO results (result,date,user_id) VALUES (?,?,?)'
        try:
            cursor.execute(query, (result, date, user_id))
            connection.commit()
            connection.close()
            return True
        except:
            return False

    @staticmethod
    def delete(result_id, user_id):
        """ DELETE A SINGLE result BASED ON ID """
        connection = connect(config.db_file)
        cursor = connection.cursor()
        query = 'DELETE FROM results WHERE id=?'
        cursor.execute(query, (result_id,))
        connection.commit()
        connection.close()
        return True

    @staticmethod
    def update(result_id, result, date):
        if Result.exist(result_id):
            connection = connect(config.db_file)
            cursor = connection.cursor()
            query = "UPDATE results SET result=?, date=? WHERE id=?"
            try:
                cursor.execute(query, (result, date, result_id))
                connection.commit()
                return True
            except:
                return False
        else:
            return False
